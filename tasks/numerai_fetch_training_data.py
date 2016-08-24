import os
import urllib2
from datetime import datetime
import zipfile

from pydblite import Base
import luigi


class DownloadTrainingData(luigi.Task):
    """
    This tasks solely fetches the datasets, if new ones are available.
    """
    dataset_path = luigi.Parameter(default='https://datasets.numer.ai/57b4899/numerai_datasets.zip')

    output_path = luigi.Parameter(default='./data/')
    database_path = luigi.Parameter(default=None)
    path = None

    def output(self):
        if not self.path:
            self._setup()

        return luigi.file.LocalTarget(self.path)

    def _setup(self):
        """
        Fetch the last modified header and determine the dataset path.
        """
        if self.database_path:
            self.db = Base(self.database_path)
        else:
            print "Skipping logging to database"

        # custom headers are needed, otherwise access is going to be forbidden
        # by cloudflare.
        req = urllib2.Request(self.dataset_path, headers={'User-Agent': "Foo"})
        self.res = urllib2.urlopen(req)

        # TODO: not really failure tolerant with the formatting. is it some
        # kind of standard? (which doesn't guarantee anything, of course)
        self.lmd = datetime.strptime(dict(self.res.info())['last-modified'],
                                     '%a, %d %b %Y %H:%M:%S %Z')

        self.fn = self.lmd.strftime('%d_%m_%Y_datasets.zip')
        self.path = os.path.join(self.output_path, self.fn)

    def run(self):
        """
        The actual task business logic. This function fetches the file from the
        already open URL and saves it to the LocalTarget (luigi specific file
        class).
        """
        print 'Saving new datasets to: %s' % (self.path,)

        with self.output().open('wb') as fp:
            # with open(self.path, 'wb') as fp:
            fp.write(self.res.read())

        if self.database_path:
            self.db.create('last_modified', 'filename', mode='open')
            rec = self.db(last_modified=self.lmd)

            if not rec:
                self.db.insert(last_modified=self.lmd, filename=self.fn)
                self.db.commit()


class FetchTrainingData(luigi.Task):
    """
    Downloads (or uses the already existing, most recent file) and extracts the
    contents of the most recent dataset. The files contained in the zipfile
    are moved to `output_path` and the files are prepended by a timestamp
    to reflect the date of the last modified header.
    """
    output_path = luigi.Parameter(default='./data/')
    database_path = luigi.Parameter(default=None)

    def requires(self):
        return DownloadTrainingData(output_path=self.output_path,
                                    database_path=self.database_path)

    def run(self):
        # input has the output of the required tasks, which in our case is only
        # one, which returns only the zipfile.
        _in = self.input()
        infn = os.path.split(_in.path)[1]

        # we explicitely parse the date to generate any exceptions without
        # doing much work.
        date = datetime.strptime(infn[0:10], '%d_%m_%Y')

        with zipfile.ZipFile(_in.path) as zf:
            for member in zf.infolist():
                # note that we are not vulnearble to the directory traversal
                # vulnerability in zipfile.extract because we only use the
                # filename of the member and ignore the path (the 0th element
                # of the split below) and use our own (given as output_path)
                filename = os.path.split(member.filename)[1]
                fn = date.strftime('%d_%m_%Y_')

                if not os.path.exists(os.path.join(self.output_path,
                                                   fn + filename)):
                    zf.extract(member, self.output_path)
                    os.rename(os.path.join(self.output_path, member.filename),
                              os.path.join(self.output_path, fn + filename))
