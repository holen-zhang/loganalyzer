import os

# with open (os.path.dirname(__file__) + "/test/diff_list_1.txt", 'r') as f:
#     content = f.read()
#     content_list = content.split(", ===")
#     content_list[0] = content_list[0][4:]
#
#     insert_number = 0
#     delete_number = 0
#     update_number = 0
#     for item in content_list:
#         list_item = item.split("\n")
#         if list_item[1] == "insert-node":
#             if list_item[3][:10] == "SimpleName":
#                 print(list_item[3][:10])
#                 print(list_item[3][12:15])
#                 if list_item[3][12:15].upper() == "LOG" or list_item[3][12:15].upper() == "LOGGER":
#                     insert_number += 1
#
#         if list_item[1] == "delete-node":
#             if list_item[3][:10] == "SimpleName":
#                 print(list_item[3][:10])
#                 print(list_item[3][12:15])
#                 if list_item[3][12:15].upper() == "LOG" or list_item[3][12:15].upper() == "LOGGER":
#                     delete_number += 1
#
#         if list_item[1] == "update-node":
#             if list_item[3][:10] == "SimpleName":
#                 print(list_item[3][:10])
#                 print(list_item[3][12:15])
#                 if list_item[3][12:15].upper() == "LOG" or list_item[3][12:15].upper() == "LOGGER":
#                     update_number += 1
#
#
#     print(insert_number)
#     print(delete_number)


def calculate_test_log_modification():
    insert_number = 0
    delete_number = 0
    update_number = 0
    for file in os.listdir("/Users/holen/DegreeProject/JsonData/Test"):
        with open("/Users/holen/DegreeProject/JsonData/Test/" + file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if content != "[]":
                content_list = content.split(", ===")
                content_list[0] = content_list[0][4:]
                print(file)
                for item in content_list:
                    list_item = item.split("\n")
                    if list_item[1] == "insert-node":
                        if list_item[3][:10] == "SimpleName":
                            # print(list_item[3][:10])
                            # print(list_item[3][12:15])
                            if list_item[3][12:15].upper() == "LOG" or list_item[3][12:15].upper() == "LOGGER":
                                insert_number += 1

                    if list_item[1] == "delete-node":
                        if list_item[3][:10] == "SimpleName":
                            # print(list_item[3][:10])
                            # print(list_item[3][12:15])
                            if list_item[3][12:15].upper() == "LOG" or list_item[3][12:15].upper() == "LOGGER":
                                delete_number += 1

                    if list_item[1] == "update-node":
                        if list_item[3][:10] == "SimpleName":
                            # print(list_item[3][:10])
                            # print(list_item[3][12:15])
                            if list_item[3][12:15].upper() == "LOG" or list_item[3][12:15].upper() == "LOGGER":
                                update_number += 1

    return insert_number, delete_number, update_number


def main():
    insert_number, delete_number, update_number = calculate_test_log_modification()
    print("Added log: " + str(insert_number))
    print("deleted log: " + str(delete_number))
    print("updated log: " + str(update_number))


if __name__  == "__main__":
    main()



