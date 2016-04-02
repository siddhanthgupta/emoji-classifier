'''
Created on 21-Mar-2016

@author: siddhanthgupta
'''
import os
import os.path
import pyinotify
import threading


class MyEventHandler(pyinotify.ProcessEvent):

    def __init__(self, classifier, depth):
        self.classifier = classifier
        self.depth = depth

    def process_IN_CREATE(self, event):
        print("CREATE event:", event.pathname)
        print(self.classifier.depth_to_score(-1, 10))
        list_emojis = []
        list_emojis.append(event.pathname.split('/')[-1][:-4])
        all_emoji_data = self.classifier.compute_and_store(
            list_emojis, self.depth)
        print('Updated stuff', all_emoji_data)

    def process_IN_DELETE(self, event):
        print("DELETE event:", event.pathname)

    def process_IN_MODIFY(self, event):
        print("MODIFY event:", event.pathname)


class ThreadFileSync(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, classifier, depth):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.directory = os.path.join(os.path.curdir, 'static/emojis')
        print(os.path.abspath(self.directory))

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread

        # watch manager
        self.wm = pyinotify.WatchManager()
        # Communicator.doc_folder
        self.watch_dict = self.wm.add_watch(
            self.directory, pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY, rec=True)

        # event handler
        eh = MyEventHandler(classifier, depth)

        # notifier
        self.notifier = pyinotify.Notifier(self.wm, eh)

        thread.start()                                  # Start the execution

    def run(self):
        self.notifier.loop()

    def remove_watch(self):
        for key, wd in self.watch_dict.items():
            self.wm.rm_watch(wd)
