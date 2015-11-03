import pypyodbc
import csv

__author__ = 'nechaev.a'

badge_conn = pypyodbc.connect('DRIVER={SQL Server}; SERVER=106.109.4.211; DATABASE=badgeID; UID=wt; PWD=samsung1')
badge_cur = badge_conn.cursor()
acc_conn1 = pypyodbc.connect('DRIVER={SQL Server}; SERVER=106.109.4.211; DATABASE=AccessControl; UID=wt; PWD=samsung1')
acc_cur1 = acc_conn1.cursor()
acc_conn2 = pypyodbc.connect('DRIVER={SQL Server}; SERVER=106.109.4.211; DATABASE=AccessControl; UID=wt; PWD=samsung1')
acc_cur2 = acc_conn2.cursor()


def list_acclvls():
    print('Getting Access Level ID:\r\n')
    acc_cur1.execute('''
                    select ACCESSLVID, DESCRIPT
                    from AccessControl.dbo.ACCESSLVL
                    ''')
    for row in acc_cur1:
        print('Access Level: "'+row[1]+'"', 'ID:', row[0])


def alvl_ex():
    print('\r\n Enter access level ID to replace')
    alvl_check = input()
    alvl = int(alvl_check)
    if not alvl_check.isdigit() or alvl_check == '0':
        print('\r\n Invalid Access Level ID!')
        alvl_ex()
    else:
        print('Access Level ID "' + alvl_check + '" will be replaced')
        return alvl


def alvl_new():
    print('\r\n Enter new access level ID:')
    alvl_check = input()
    alvl = int(alvl_check)
    if not alvl_check.isdigit() or alvl_check == '0':
        print('\r\n Invalid Access Level ID!')
        alvl_new()
    else:
        print('Access Level will be updated with ID "' + alvl_check + '"')
        return alvl


def alvl_update():
    with open('badgeID.csv', newline='') as csvfile:
        listreader = csv.reader(csvfile, delimiter=';')
        for badge_id in listreader:
            acc_cur1.execute('''
                            select BADGEKEY
                            from AccessControl.dbo.BADGE
                            where ID = ?
                            ''', [int(badge_id[0])])
            for badge_key in acc_cur1:
                acc_cur2.execute('''
                                update AccessControl.dbo.BADGELINK
                                set ACCLVLID = ?
                                where BADGEKEY = ? and ACCLVLID = ?
                                ''', [alvl_rep, badge_key[0], alvl_old])
                print('Badge', badge_id[0], 'updated')
                acc_conn2.commit()


list_acclvls()

alvl_old = alvl_ex()
alvl_rep = alvl_new()

alvl_update()

badge_conn.close()
acc_conn1.close()
acc_conn2.close()

# def alvl_update():
#     badge_cur.execute('''
#                     select ID
#                     from badgeID.dbo.badgeID
#                     ''')
#     for badge_id in badge_cur:
#         acc_cur1.execute('''
#                         select BADGEKEY
#                         from AccessControl.dbo.BADGE
#                         where ID = ?
#                         ''', badge_id)
#         for badge_key in acc_cur1:
#             acc_cur2.execute('''
#                             update AccessControl.dbo.BADGELINK
#                             set ACCLVLID = ?
#                             where BADGEKEY = ? and ACCLVLID = 2
#                             ''', [alvl_res, badge_key[0]])
#             print(acc_cur2.rowcount, 'badges updated')
#             acc_conn2.commit()
#
#
# list_acclvls()
#
# alvl_res = alvl_input()
#
# alvl_update()
#
# badge_conn.close()
# acc_conn1.close()
# acc_conn2.close()
