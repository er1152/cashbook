from models import *
import db
import os
 
 
if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):
 
        Base.metadata.create_all(db.engine)
 
    # サンプルitem
    sample_item = Item(
        date=datetime(2022, 1, 16),
        cost=500,
        detail='弁当',
        category='食費',
        is_in=False
    )

    db.session.add(sample_item)
    db.session.commit()
    db.session.close()  