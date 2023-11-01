

def init_fake_db():
    return{
        "users": {},
        # "users": init_data_from_file("storage/users.json"),
        #"discussions": nit_data_from_file("storage/discussions.json"),
        #"messages": init_data_from_file("storage/messages.json")
    }
fake_db = init_fake_db()