from pydantic import BaseModel, Field

# class Section(BaseModel):
# 	title: str
# 	content: str

class HtmlContent(BaseModel):
	page_title: str
	content: str
