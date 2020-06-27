
class ArticleDetails:
    def __init__(self, iid, header, createdAt, updatedAt, subject, sub_subject):
        self.iid = iid
        self.siteId = ''
        self.header = header
        self.createdAt = createdAt
        self.updatedAt = updatedAt

        self.subject = subject
        self.subSubject = sub_subject

        self.url = ''
        self.originalUrl = ''

        self.subHeader = ''
        self.description = ''
        self.type = 'HTML'
        self.site = 'Haaretz'
        self.author = ''
        self.image1 = ''
        self.image2 = ''
        self.thumbnail = ''

