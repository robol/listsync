class DummyServer():
    def get_members(self, list_name):
        return []

    def add_member(self, list_name, email_address):
        print("Dummy adding {} to {}".format(email_address, list_name))
        return True

    def delete_member(self, list_name, email_address):
        print("Dummy delete {} from {}".format(email_address, list_name))
        return True