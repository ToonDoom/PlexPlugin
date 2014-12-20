import unittest

from plexapi import PlexApi
from mock import Mock


class MockIndigo():
    def __init__(self):
        pass

    @staticmethod
    def debugLog(text):
        print(text)


class TestPlexApi(unittest.TestCase):
    # def setUp(self):

    def testGetClientMachineIds(self):
        real = PlexApi("foo", "bar")
        machineId1 = '''TestMI1'''
        machineId2 = '''TestMI2'''
        real.getStatusSession = Mock(return_value=('''
                <MediaContainer size="1">
                    <Video>
                        <Player machineIdentifier="%s" platform="Plex Home Theater" product="Plex Home Theater" state="paused" title="HTPC" />
                        <Player machineIdentifier="%s" platform="Plex Home Theater" product="Plex Home Theater" state="paused" title="HTPC" />
                    </Video>
                </MediaContainer>
            ''' % (machineId1, machineId2)))

        machineIds = real.getClientMachineIds()
        assert isinstance(machineIds, list)
        self.assertEqual(2, len(machineIds))
        self.assertEqual(machineId1, machineIds[0])
        self.assertEqual(machineId2, machineIds[1])

    def testGetClientMachineIds_no_results(self):
        real = PlexApi("foo", "bar")
        real.getStatusSession = Mock(return_value='''
                <MediaContainer size="0">
                </MediaContainer>
            ''')

        machineIds = real.getClientMachineIds()
        assert isinstance(machineIds, list)
        self.assertEqual(0, len(machineIds))

    def testGetClientState(self):
        real = PlexApi("foo", "bar")
        machineId1 = 'TestMI1'
        machineId2 = 'TestMI2'
        real.getStatusSession = Mock(return_value=('''
                <MediaContainer size="1">
                    <Video>
                        <Player machineIdentifier="%s" platform="Plex Home Theater" product="Plex Home Theater" state="paused" title="HTPC" />
                        <Player machineIdentifier="%s" platform="Plex Home Theater" product="Plex Home Theater" state="playing" title="HTPC" />
                    </Video>
                </MediaContainer>
            ''' % (machineId1, machineId2)))

        state = real.getClientState(machineId1)
        self.assertEqual('paused', state)
        state = real.getClientState(machineId2)
        self.assertEqual('playing', state)
        state = real.getClientState('unknownMI')
        self.assertEqual('client_offline', state)

    # def testGetClientMachineIds_dummy(self):
    #     plexServer = "192.168.0.6"
    #     plexPort = "32400"
    #
    #     real = PlexApi(plexServer, plexPort)
    #     # real.getStatusSession = Mock(return_value='''
    #     #         <MediaContainer size="0">
    #     #         </MediaContainer>
    #     #     ''')
    #
    #     try:
    #         machineIds = real.getClientMachineIds(MockIndigo)
    #         foo = 1
    #     except Exception, e:
    #         print(u"Failed: " + str(e) + u")")





        # def test_choice(self):
        # element = random.choice(self.seq)
        # self.assertTrue(element in self.seq)
        #
        # def test_sample(self):
        #     with self.assertRaises(ValueError):
        #         random.sample(self.seq, 20)
        #     for element in random.sample(self.seq, 5):
        #         self.assertTrue(element in self.seq)


if __name__ == '__main__':
    unittest.main()