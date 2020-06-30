from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


# using pydrive. see https://towardsdatascience.com/how-to-manage-files-in-google-drive-with-python-d26471d91ecd
# to get the authorization needed, get values of client_id and client_secret as described here:
# https://www.iperiusbackup.net/en/how-to-enable-google-drive-api-and-get-client-credentials/
# and put them in the settings.yaml file.
# this project contains a settings.template.yaml file

FOLDER = "'application/vnd.google-apps.folder'"
is_folder = "mimeType = " + FOLDER + " "
AND = " and "

def query_children_of(id):
  return "'" + id + "' in parents"

def title(x):
  return x['title']


def folders(drive):


  folder_list = drive.ListFile({'q': is_folder + AND +
                                   "'root' in parents " + AND +
                                   "title='videoCourses'",
                              'fields':'items(id, title)', 'maxResults': 2}).GetList()
                              #'fields':'items(id, title, parents)', 'maxResults': 9})
  count = 0

  id_of_root = list(folder_list).pop(0)['id']
  # for item in folder_list:
  #   count = count + 1
  #   print(count, item)
  #   the_id = item['id']

  # file6 = drive.CreateFile({'id': the_id})
  # p = file6['title']
  # print(p)

  query = query_children_of(id_of_root)
  folders_under_videoCourses = drive.ListFile({'q': query_children_of(id_of_root), 'fields':'items(id, title)', 'maxResults': 500}).GetList()
  x = len(list(folders_under_videoCourses))
  print("found " + str(x) + " subdirs")
  if (x > 500):
    print("more than 500 sub-dirs of videoCourses! fix the code of the query!!!")
    return
  # for item in folders_under_videoCourses:
  #   count = count + 1
  #   print(count, item)

  titles = list(map(title, folders_under_videoCourses))
  print(titles)
  # for x in titles:
  #   print(x)


def properties_of_files(drive):
  file_list = drive.ListFile({'q': 'trashed=false', 'maxResults': 2, 'fields': ['title, id']}).GetList()
  for file1 in file_list:
    print('')
    print('')
    print('==============================')
    print('title: %s, id: %s' % (file1['title'], file1['id']))
    # print (file1.GetPermissions())  # ==> userPermission

    for prop in ['parents', 'ownerNames']:
      print('%s: %s' % (prop, file1.get(prop)))
    for prop in ['mimeType',
                 'createdDate', 'modifiedDate',
                 'fileSize', 'originalFilename', 'fileExtension',
                 'videoMediaMetadata', 'appDataContents',
                 'kind', 'etag', 'selfLink', 'webContentLink', 'alternateLink', 'embedLink', 'iconLink',
                 'thumbnailLink',
                 # title, id,
                 'content',  # - may be None,
                 'copyRequiresWriterPermission', 'markedViewedByMeDate', 'version',
                 'downloadUrl', 'md5Checksum', 'quotaBytesUsed', 'lastModifyingUserName',
                 'editable', 'copyable', 'writersCanShare', 'shared', 'spaces',
                 # dictionaries:
                 'userPermission', 'capabilities',  # 'gauthattr',
                 'lastModifyingUser', 'metadata',
                 'labels'
                 ]:
      if prop in file1:
        print('%s : %s' % (prop, file1.get(prop)))
      else:
        print(prop)

  # lastModifyingUser{},capabilities{} gauthattr{} metadata{}  # labels{}


def main():
  gauth = GoogleAuth()

  ###
  # This works because:
  # we have in the current dir a file "settings.yaml"
  # and we have in the current dir a file "credentials.json"
  # (otherwise - would not be authorized to access my google drive!)
  # these files should NOT be pushed to Git!!
  drive = GoogleDrive(gauth)
  folders(drive)
  return






main()
