"""
main.py
Demo driver that runs every functional requirement (FR-01 to FR-10).
Run with:  python main.py
"""

from models import LibrarySystem


def main():
    lib = LibrarySystem()

    # FR-08 add books
    lib.add_book("B1", "Data Structures", "Mark Allen", "CS", "111")
    lib.add_book("B2", "Clean Code", "Robert Martin", "SE", "222")
    lib.add_book("B3", "Operating Systems", "Silberschatz", "CS", "333")
    print("FR-08 Books in catalogue:", len(lib.books))

    # FR-01 register, FR-02 login
    print("FR-01", lib.register("M1", "Ali", "ali@uni.edu", "pass123"))
    print("FR-02 Login:", lib.login("ali@uni.edu", "pass123"))
    print("FR-02 Wrong password:", lib.login("ali@uni.edu", "wrong"))

    # FR-03 search, FR-04 details
    print("FR-03 Search 'CS':", [b.title for b in lib.search("CS")])
    print("FR-04 Details:", lib.details("B1"))

    # FR-05 borrow, FR-06 return
    print("FR-05", lib.borrow("M1", "B1"))
    print("FR-05 again:", lib.borrow("M1", "B1"))
    print("FR-06", lib.return_book("M1", "B1"))

    # FR-07 history
    lib.borrow("M1", "B2")
    print("FR-07 History:", lib.history("M1"))

    # FR-09 manage member
    print("FR-09", lib.manage_member("M1", "Suspended"))

    # FR-10 recommendations
    lib.borrow("M1", "B1")
    print("FR-10 Recommend:", lib.recommend("M1"))


if __name__ == "__main__":
    main()
