class Journal:
    ''' Constructor de la clase Journal '''
    def __init__(self, id, title, areas, catalogs, website, h_index, subjet_area_and_category, publisher, issn, widget, publication_type):
        self.id = id
        self.title = title
        self.areas = areas
        self.catalogs = catalogs
        self.website = website
        self.h_index = h_index
        self.subjet_area_and_category = subjet_area_and_category
        self.publisher = publisher
        self.issn = issn
        self.widget = widget
        self.publication_type = publication_type