import detector
import os

class testosshim:

    def __init__(self, folder):
        self.folder = folder
    
    def movieFolder(self):
        return r"C:\Media\\Movies\\"

    def tvFolder(self):
        return r"C:\Media\TV\\"

    def link(self, source, target):
        return "Linking " + source + " => " + target


    def listdir(self, path):
        parts = os.path.normpath(path).split(os.path.sep)
        
        cd = self.folder

        for part in parts:
            if (cd.has_key(part)):
                cd = cd[part]
            else:
                return []

        return cd.keys()

    def isdir(self, path):
        parts = os.path.normpath(path).split(os.path.sep)
        
        cd = self.folder

        for part in parts[:-1]:
            if (cd.has_key(part)):
                cd = cd[part]
            else:
                return False
        if (not cd.has_key(parts[-1])):
            return False

        return cd[parts[-1]] != True

    def extract(self, source, target):
        return "Extracting " + source + " => " + target

    def getApiKey(self):
        return ""

fstruct = {
    "C:" : {
        "downloads" : {
            "test.movie.2017.UHD.1337.mkv":True,
            "test.show.s01e01.mkv":True,
            "test.show.format2.s1e1.mkv":True,
            "Test.Show.3.S01E02": {
                "test.show.3.s01e02.part1.rar":True,
                "test.show.3.s01e02.part2.rar":True,
                "test.show.3.s01e02.part3.rar":True,
            },
            "The.Test.Show.With.Yo.Momma.2017.03.22.Yo.Momma":{
                "The.Test.Show.With.Yo.Momma.2017.03.22.Yo.Momma.r01": True,
                "The.Test.Show.With.Yo.Momma.2017.03.22.Yo.Momma.r02": True,
                "The.Test.Show.With.Yo.Momma.2017.03.22.Yo.Momma.r03": True,
                "The.Test.Show.With.Yo.Momma.2017.03.22.Yo.Momma.rar": True
            },
            "Test.Movie.23.2017.UHD.1337": {
                "Subs": {
                    "Test.Movie.23.2017.UHD.1337.part1.rar":True,
                },
                "Test.Movie.23.2017.UHD.1337.part1.rar":True,
                "Test.Movie.23.2017.UHD.1337.part2.rar":True,
                "Test.Movie.23.2017.UHD.1337.part3.rar":True,
                "Test.Movie.23.2017.UHD.1337.sample.mkv":True,
                "Test.Movie.23.2017.UHD.1337.sfv":True
            },
            "Don't look down": {
                "Don't look down 1080p.mkv": True
            },
            "S01_-_Complete": {
                "Show.Name.1x01.The_Stakeout.DVDRip_Xvid-Fov": {
                    "Show.Name.1x01.The_Stakeout.DVDRip_Xvid-Fov.r00": True,
                    "Show.Name.1x01.The_Stakeout.DVDRip_Xvid-Fov.r01": True,
                    "Show.Name.1x01.The_Stakeout.DVDRip_Xvid-Fov.rar": True,
                },
                "Show.Name.1x02.The_Stakeout.DVDRip_Xvid-Fov": {
                    "Show.Name.1x02.The_Stakeout2.DVDRip_Xvid-Fov.r00": True,
                    "Show.Name.1x02.The_Stakeout2.DVDRip_Xvid-Fov.r01": True,
                    "Show.Name.1x02.The_Stakeout2.DVDRip_Xvid-Fov.rar": True,
                },
            },
            "Season_11-COMPLETE": {
                "Show.Name.11x01.The_Stakeout.DVDRip_Xvid-Fov": {
                    "sn11ep1-yd.r00": True,
                    "sn11ep1-yd.r01": True,
                    "sn11ep1-yd.rar": True,
                },
                "Show.Name.1x02.The_Stakeout.DVDRip_Xvid-Fov": {
                    "sn11ep2-yd.r00": True,
                    "sn11ep2-yd.r01": True,
                    "sn11ep2-yd.rar": True,
                },
            },
            "The Show - Complete": {
                "The Show - Season 1" : {
                    "Show, The - S1E01 - Pilot.avi": True,
                    "Show, The - S1E02 - Second.avi":True,
                },
                "The Show - Season 2" : {
                    "Show, The - S2E01 - Pilot.avi": True,
                    "Show, The - S2E02 - Second.avi":True,
                }
            }
        },
        "Media": {
            "Movies": {

            },
            "TV": {

            }
        }
    }
}
shim = testosshim(fstruct)

#print(detector.detect("Test.Show.3.S01E02", "C:\\downloads\\", shim))
#print(detector.detect("test.show.s01e01.mkv", "C:\\downloads\\", shim))
#print(detector.detect("The.Test.Show.With.Yo.Momma.2017.03.22.Yo.Momma", "C:\\downloads\\", shim))

# print(detector.detect("Don't look down", "C:\\downloads\\", shim))
# print(detector.detect("Test.Movie.23.2017.UHD.1337", "C:\\downloads\\", shim))
# print(detector.detect("S01_-_Complete", "C:\\downloads\\", shim))
# print(detector.detect("Season_11-COMPLETE", "C:\\downloads\\", shim))
print(detector.detect("The Show - Complete", "C:\\downloads\\", shim))