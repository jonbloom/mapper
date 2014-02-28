class Quote(object):
	def __init__(self,id,title,quote,isbn,page_no,tags):
		self.id = id
		self.quote = quote
		self.title = title
		self.isbn = isbn
		self.page_no = page_no
		self.tags = tags
	def __repr__(self):
		return self.title + ", " + self.quote + ", tags: " + ", ".join(self.tags)
	def comma_tags(self):
		for t in tags:
			t.strip()
		return ", ".join(self.tags)