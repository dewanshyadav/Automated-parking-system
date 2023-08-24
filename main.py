import mysql.connector
import time
from datetime import date
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr


global conn, cursor
conn = mysql.connector.connect(
    host='localhost', database='parking_system', user='root', password='tiger')
cursor = conn.cursor()

def anpd():

    print("\n1.  System generated image")
    print("\n2.  Capture using camera")
    choice = int(input('Enter your choice ...: '))

    if choice==1:
        img = cv2.imread('image1.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))

        bfilter = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise reduction
        edged = cv2.Canny(bfilter, 30, 200)  # Edge detection
        plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break

        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)


        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)
        text = result[0][-2]
        print("Number plate: ",text)

        font = cv2.FONT_HERSHEY_SIMPLEX
        res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[0][0][1] + 60), fontFace=font, fontScale=1,
                          color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0, 255, 0), 5)
        plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
        plt.title("Frame")
        plt.show()
        return text
    if choice==2:
        text=cam()
        return text

def cam():
    vid = cv2.VideoCapture(0)
  
    while(True):
          
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
      
        # Display the resulting frame
        cv2.imshow('frame', frame)
        cv2.imwrite("camimage.jpg",frame) 
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
      
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

    img = cv2.imread('camimage.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))

    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise reduction
    edged = cv2.Canny(bfilter, 30, 200)  # Edge detection
    plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break

    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    text = result[0][-2]
    print("Number plate: ",text)

    font = cv2.FONT_HERSHEY_SIMPLEX
    res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[0][0][1] + 60), fontFace=font, fontScale=1,
                      color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0, 255, 0), 5)
    plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
    plt.title("Frame")
    plt.show()
    return text

    
def clear():
    for _ in range(50):
        print()


def made_by():
    msg = ''' 
            Parking Management system made by           : DEWANSH YADAV
            \n\n\n
        '''

    for x in msg:
        print(x, end='')
        time.sleep(0.002)

    wait = input('Press any key to continue.....')


def display_parking_type_records():
    cursor.execute('select * from parking_type;')
    records = cursor.fetchall()
    for row in records:
        print(row)
    wait = input('\n\n\nPress any key to continue............')


def login():

    while True:
        clear()
        uname = input('Enter your ID :')
        upass = input('Enter your Password :')
        #upass = stdiomask.getpass()
        cursor.execute('select * from login where name="{}" and pwd ="{}"'.format(uname, upass))
        cursor.fetchall()
        rows = cursor.rowcount
        if rows != 1:
            print('Invalid Login details..... Try again')
        else:
            print('You are eligible for operating this system............')
            print('\n\n\n')
            print('Press any key to continue...............')
            break




def add_parking_type_record():
    clear()
    name = input('Enter Parking Type : ')
    cursor.execute('select name from parking_type')
    name2 = cursor.fetchall()
    print("Already Available types")
    print(name2)
    price = input('Enter Parking Price per day : ')
    sql = 'insert into parking_type(name,price) values("{}",{});'.format(name, price)
    cursor.execute(sql)
    print('\n\n New Parking Type added....')
    cursor.execute('select max(type_id) from parking_type')
    no = cursor.fetchone()
    print(' New Parking Type ID is : {} \n\n\n'.format(no[0]))
    wait = input('\n\n\nPress any key to continue............')


def add_parking_slot_record():
    clear()
    parking_type_id = input(
        'Enter Parking Type( 1. Two wheelar 2. Car 3. Bus 4. Truck 5. Trolly ) :')
    status = input('Enter current Status ( Open/Full ) :')
    sql = 'insert into parking_space(type_id,status) values \
            ("{}","{}");'.format(parking_type_id, status)
    cursor.execute(sql)
    print('\n\n New Parking Space Record added....')

    cursor.execute('select max(slot) from parking_space;')
    no = cursor.fetchone()
    print(' Your Parking ID is : {} \n\n\n'.format(no[0]))
    display_parking_type_records()
    wait = input('\n\n\nPress any key to continue............')


def modify_parking_type_record():
    clear()
    print(' M O D I F Y   P A R K I N G   T Y P E  S C R E E N ')
    print('-' * 100)
    print('1.  Parking Type Name \n')
    print('2.  Parking Price  \n')
    choice = int(input('Enter your choice :'))
    field = ''
    if choice == 1:
        field = 'name'
    if choice == 2:
        field = 'price'

    park_id = input('Enter Parking Type ID :')
    value = input('Enter new values :')
    sql = 'update parking_type set ' + field + ' = ' + value + ' where typ =' + park_id + ';'
    cursor.execute(sql)
    print('Record updated successfully................')
    display_parking_type_records()
    wait = input('\n\n\nPress any key to continue............')


def modify_parking_space_record():
    clear()
    print(' M O D I F Y  P A R K I N G   S P A C E   R E C O R D ')
    print('-' * 100)
    print('1.  Parking Type ID(1-Two Wheelar, 2: Car 3.Bus etc ):  ')
    print('2.  status  \n')
    choice = int(input('Enter your choice :'))
    field = ''
    if choice == 1:
        field = 'type_id'
    if choice == 2:
        field = 'status'
    print('\n\n\n')
    crime_id = input('Enter Parking Space ID  :')
    value = input('Enter new values :')
    sql = 'update parking_space set ' + field + \
          ' = "' + value + '" where slot =' + crime_id + ';'
    cursor.execute(sql)
    print('Record updated successfully................')
    wait = input('\n\n\nPress any key to continue............')


def add_new_vehicle():
    clear()
    print('Vehicle Login Screen ')
    print('-' * 100)
    vehicle_id = anpd()
    type_id = input('Enter vehicle type :')
    sql = 'select slot from parking_space where type_id = {} AND status = "open"'.format(type_id)
    cursor.execute(sql)
    vacant = cursor.fetchall()
    if vacant != []:
        vlist=[]
        print("Vacant palces: ", end="")
        for i in vacant:
            print(i[0], end="  ")
            vlist.append(i[0])
        # print(vlist)l
        # print(type(vlist[1]))
        parking_id = int(input('Enter parking slot :'))
        if parking_id in vlist:
            entry_date = date.today()
            sql = 'insert into transaction(vehicle_id,parking_id,entry_date) values \
                       ("{}","{}","{}");'.format(vehicle_id, parking_id, entry_date)
            cursor.execute(sql)
            cursor.execute('update parking_space set status ="full" where slot ={}'.format(parking_id))
            print('\n\n\n Record added successfully.................')
        else:
            print("Invalid entry!!! space already reserved")
    else:
        print("NO PLACE VACANT FOR THIS TYPE VEHICLE")
    wait = input('\n\n\nPress any key to continue.....')


def remove_vehicle():
    clear()
    print('Vehicle Logout Screen')
    print('-' * 100)
    vehicle_id = input('Enter vehicle No :')
    exit_date = date.today()
    sql = 'select parking_id,price,entry_date from transaction tr,parking_space ps, parking_type pt \
           where tr.parking_id = ps.slot and ps.type_id = pt.type_id and \
           vehicle_id ="' + vehicle_id + '" and exit_date is NULL;'
    cursor.execute(sql)
    record = cursor.fetchone()
    days = (exit_date - record[2]).days
    if days == 0:
        days = days + 1
    amount = record[1] * days
    clear()
    print('Logout Details ')
    print('-' * 100)
    print('Parking ID : {}'.format(record[0]))
    print('Vehicle ID : {}'.format(vehicle_id))
    print('Parking Date : {}'.format(record[2]))
    print('Current Date : {}'.format(exit_date))
    print('Amount Payable : {}'.format(amount))
    wait = input('press any key to continue......')
    # update transaction and parking space tables
    sql1 = 'update transaction set exit_date ="{}" , amount ={} where vehicle_id ="{}" \
            and exit_date is NULL;'.format(exit_date, amount, vehicle_id)
    sql2 = 'update parking_space set status ="open" where slot = {}'.format(record[0])
    cursor.execute(sql1)
    cursor.execute(sql2)
    wait = input('Vehicle Out from our System Successfully.......\n Press any key to continue....')


def search_menu():
    clear()
    print(' S E A R C H  P A R K I N G  M E N U ')
    print('1.  Parking ID \n')
    print('2.  Vehicle Parked  \n')
    print('3.  Free Space \n')
    choice = int(input('Enter your choice :'))
    if choice == 2:
        sql = 'select vehicle_id,parking_id,entry_date from transaction where exit_date is NULL;'
    if choice == 3:
        parking_status("open")
        return
        
    if choice == 1 :
        value = input('Enter value to search :')
        sql = 'select ps.slot,name,price, status \
          from parking_space ps , parking_type pt where ps.type_id = pt.type_id AND ps.slot ={}'.format(value)
        

    cursor.execute(sql)
    results = cursor.fetchall()
    records = cursor.rowcount
    for row in results:
        print(row)
    if records < 1:
        print('Record not found \n\n\n ')
    wait = input('\n\n\nPress any key to continue......')


def parking_status(status):
    clear()
    print('Parking Status :', status)
    print('-' * 100)
    sql = "select * from parking_space where status ='{}'".format(status)
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:
        print(row)
    wait = input('\n\n\nPress any key to continue.....')


def vehicle_status_report():
    clear()
    print('Vehicle Status - Currently Parked')
    print('-' * 100)
    sql = 'select * from transaction where exit_date is NULL;'
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:
        print(row)
    wait = input('\n\n\nPress any key to continue.....')


def money_collected():
    clear()
    start_date = input('Enter start Date(yyyy-mm-dd): ')
    end_date = input('Enter End Date(yyyy-mm-dd): ')
    sql = "select sum(amount) from transaction where \
          entry_date >='{}' and exit_date <='{}'".format(start_date, end_date)
    cursor.execute(sql)
    result = cursor.fetchone()
    print('Total money Collected from {} to {}'.format(start_date, end_date))
    print('-' * 100)
    print(result[0])
    wait = input('\n\n\nPress any key to continue.....')


def report_menu():
    while True:
        clear()
        print(' P A R K I N G    R E P O R T S  ')
        print('-' * 100)
        print('1.  Parking Types \n')
        print('2.  Free Space  \n')
        print('3.  Ocupied Space  \n')
        print('4.  Vehicle Status  \n')
        print('5.  Money Collected  \n')
        print('6.  Exit  \n')
        choice = int(input('Enter your choice :'))
        field = ''
        if choice == 1:
            display_parking_type_records()
        if choice == 2:
            parking_status("open")
        if choice == 3:
            parking_status("full")
        if choice == 4:
            vehicle_status_report()
        if choice == 5:
            money_collected()
        if choice == 6:
            break


def main_menu():
    clear()
    login()

    
    while True:
        clear()
        print(' P A R K I N G   M A N A G E M E N T    S Y S T E M')
        print('*' * 100)
        print("\n1.  Add New Parking Type")
        print("\n2.  Add New Parking Slot")
        print('\n3.  Modify Parking Type Record')
        print('\n4.  Modify Parking Slot Record')
        print('\n5.  Vehicle Login ')
        print('\n6.  Vehicle Logout')
        print('\n7.  Search menu')
        print('\n8.  Report menu')
        print('\n9.  Close application')
        print('\n\n')
        choice = int(input('Enter your choice ...: '))

        if choice == 1:
            add_parking_type_record()

        if choice == 2:
            add_parking_slot_record()

        if choice == 3:
            modify_parking_type_record()

        if choice == 4:
            modify_parking_space_record()

        if choice == 5:
            add_new_vehicle()

        if choice == 6:
            remove_vehicle()

        if choice == 7:
            search_menu()

        if choice == 8:
            report_menu()

        if choice == 9:
            break
    made_by()


if __name__ == "__main__":
    main_menu()
