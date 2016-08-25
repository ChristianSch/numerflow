import os
import urllib2
from datetime import datetime
import zipfile

import luigi


class FetchAndExtractData(luigi.Task):
    """
    Fetches the most recent datasets and extracts the contents. The files
    contained in the zipfile are moved to `output_path` and the files are
    prepended by a timestamp to reflect the date of the last modified header.
    """
    dataset_path = luigi.Parameter(
        default='https://datasets.numer.ai/57b4899/numerai_datasets.zip')
    output_path = luigi.Parameter(default='./data/')

    def output(self):
        # custom headers are needed, otherwise access is going to be forbidden
        # by cloudflare.
        req = urllib2.Request(self.dataset_path, headers={'User-Agent': "Foo"})
        self.res = urllib2.urlopen(req)

        # TODO: not really failure tolerant with the formatting. is it some
        # kind of standard? (which doesn't guarantee anything, of course)
        lmd = datetime.strptime(dict(self.res.info())['last-modified'],
                                '%a, %d %b %Y %H:%M:%S %Z')

        prefix = lmd.strftime('%d_%m_%Y')

        dataset_path = os.path.join(self.output_path,
                                    '{0}_dataset.zip'.format(prefix))
        test_data_path = os.path.join(self.output_path,
                                      '{0}_training_data.csv'.format(prefix))
        tournament_data_path = os.path.join(self.output_path,
                                            '{0}_tournament_data.csv'
                                            .format(prefix))
        example_data_path = os.path.join(self.output_path,
                                         '{0}_example_predictions.csv'
                                         .format(prefix))

        return {
            'zipfile': luigi.LocalTarget(dataset_path),
            'training_data.csv': luigi.LocalTarget(test_data_path),
            'tournament_data.csv': luigi.LocalTarget(tournament_data_path),
            'example_predictions.csv': luigi.LocalTarget(example_data_path)
        }

    def run(self):
        out = self.output()

        with out['zipfile'].open('wb') as fp:
            fp.write(self.res.read())

        with zipfile.ZipFile(out['zipfile'].path) as zf:
            for member in zf.infolist():
                # note that we are not vulnearble to the directory traversal
                # vulnerability in zipfile.extract because we only use the
                # filename of the member and ignore the path (the 0th element
                # of the split below) and use our own (given as output_path)
                filename = os.path.split(member.filename)[1]

                if 'numerai_' in filename:
                    target_name = filename.replace('numerai_', '')
                else:
                    target_name = filename

                target = out[target_name]
                zf.extract(member, self.output_path)
                os.rename(os.path.join(self.output_path, member.filename),
                          target.path)
