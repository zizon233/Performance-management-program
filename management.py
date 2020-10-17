import sys
import os

def list_format():  # 성적 출력 포맷
    print('%10s%20s%12s%8s%10s%8s' % ('Student', 'Name', 'Midterm', 'Final', 'Average', 'Grade'))
    print('-' * 68)

def calc_average(*a):  # 평균 값 계산 함수
    n = len(a)
    sum = 0
    for i in a:
        sum += int(i)
    return sum/n

def calc_grade(x):  # 등급 계산 함수
    if x >= 90:
        return 'A'
    elif x >= 80:
        return 'B'
    elif x >= 70:
        return 'C'
    elif x >= 60:
        return 'D'
    else:
        return 'F'

def show(sortStu, grade='All'):  # 성적 데이터 출력
    list_format()
    for x in sortStu:
        if x[1][4] == grade or grade == 'All':  # searchgrade 함수와 연동하여 조건에 따라 데이터 출력
            print('%10s' % x[0], end='')
            print('%20s%10s%9s%10s%7s' % (x[1][0], x[1][1], x[1][2], x[1][3], x[1][4]))

def search(stuInfo, stuID = '', order='search'):  # 학생번호를 바탕으로 데이터 찾는 함수
    if stuID == '':
        stuID = input('Students ID: ')
        if stuInfo.get(stuID) == None:
            print('NO SUCH PERSON.')
            return None
        elif order != 'search':  # 본래의 함수가 아니라면 학생번호를 반환해줌
            return stuID
    list_format()
    x = stuInfo[stuID]
    print('%10s' % stuID, end='')
    print('%20s%10s%9s%10s%7s' % (x[0], x[1], x[2], x[3], x[4]))

def changescore(stuInfo):  # 학생번호로 중간점수 기말점수를 선택해 바꿔주는 함수
    stuID = search(stuInfo, '', '1')
    if stuID == None:
        return
    exam = input('Mid/Final? ')
    exam = exam.lower()
    if exam == 'mid':
        score = int(input('Input new score: '))
        if score < 0 or score > 100:  # 점수가 0~100 사이가 아니라면 함수 탈출
            return
        search(stuInfo, stuID)
        stuInfo[stuID][1] = str(score)  # 정보 수정
        ave = calc_average(stuInfo[stuID][1],stuInfo[stuID][2])
        stuInfo[stuID][3] = ave
        stuInfo[stuID][4] = calc_grade(ave)
        print('Score changed.')
        search(stuInfo, stuID)
    elif exam == 'final':
        score = int(input('Input new score: '))
        if score < 0 or score > 100:
            return
        search(stuInfo, stuID)
        stuInfo[stuID][2] = str(score)
        ave = calc_average(stuInfo[stuID][1], stuInfo[stuID][2])
        stuInfo[stuID][3] = ave
        stuInfo[stuID][4] = calc_grade(ave)
        print('Score changed.')
        search(stuInfo, stuID)
    else:
        return

def searchgrade(sortStu):  # 등급을 바탕으로 학생정보 출력하는 함수
    grade = input('Grade to search: ')
    if grade == 'A' or grade == 'B' or grade == 'C' or grade == 'D' or grade == 'F':
        check = 0
        for x in sortStu:  # 입력된 등급에 해당된 학생정보가 있는지 확인하는 반복문
            if x[1][4] == grade or grade == 'All':
                check = 1
        if check:
            show(sortStu, grade)
        else:
            print('NO RESEULTS.')
            return
    else:
        return

def add(stuInfo):  # 학생정보를 추가하는 함수
    stuID = input('Student ID: ')
    if stuInfo.get(stuID):
        print('ALREADY EXISTS.')
        return
    Name = input('Name: ')
    mid = input('Midterm Score: ')
    final = input('Final Score: ')
    ave = calc_average(mid, final)
    stuli = [Name, mid, final, ave, calc_grade(ave)]
    stuInfo[stuID] = stuli
    print('Student added.')

def remove(stuInfo):  # 학생번호로 학생정보를 삭제하는 함수
    if len(stuInfo) == 0:
        print('List is empty.')
        return
    stuID = search(stuInfo, '', 'remove')
    if stuID == None:
        return
    else:
        del stuInfo[stuID]
        print('Student removed.')

def quit(sortStu):  # 프로그램 종료 함수
    saveData = input('Save data?[Yes/no] ')
    saveData = saveData.lower()
    if saveData == 'yes':
        fileName2 = input('File name: ')  # 성적 정보 저장
        with open(fileName2, 'w') as f:
            for stu in sortStu:
                f.write(str(stu[0])+'\t'+str(stu[1][0])+'\t'+str(stu[1][1])+'\t'+str(stu[1][2])+'\n')
    else:
        return

stuInfo = {}  # 학생정보를 저장하기 위한 딕셔너리 변수
filename = 'students.txt'
if len(sys.argv)>1:
    filename = str(sys.argv[1])
if os.path.exists('./%s' % filename):
    with open(filename, 'r') as f:
        for line in f:
            lineLi = line.split()
            aveValue = calc_average(lineLi[3], lineLi[4])
            stuInfo[lineLi[0]] = [lineLi[1]+' '+lineLi[2], lineLi[3], lineLi[4], aveValue, calc_grade(aveValue)]

    sortStu = sorted(stuInfo.items(), key=lambda x: x[1][3], reverse=True)
    show(sortStu)

    while True:
        sortStu = sorted(stuInfo.items(), key=lambda x: x[1][3], reverse=True)
        print('\n#', end=' ')
        order = input()
        order = order.lower()
        if order == 'show':
            show(sortStu)
        elif order == 'search':
            search(stuInfo, '')
        elif order == 'changescore':
            changescore(stuInfo)
        elif order == 'searchgrade':
            searchgrade(sortStu)
        elif order == 'add':
            add(stuInfo)
        elif order == 'remove':
            remove(stuInfo)
        elif order == 'quit':
            quit(sortStu)
            break
        else:
            continue

else:
    print('NO SUCH FILE')