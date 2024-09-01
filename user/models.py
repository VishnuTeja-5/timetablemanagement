from django.db import models

# Create your models here.


class Branch:
    bid : int
    bname : str


class Subject:
    subid : int
    subcode : str
    subname : str
    subl : int
    subt : int
    subp : int
    subdep : str
    subyear : str
    subsem : str
    subreg : str


class Faculty:
    fid : int
    fname : str
    funame : str
    contact : str
    branches : str


class FS:
    fsid : int
    fname : str
    sname : str
    dep : str
    year : str
    sec : str
    ay : str

class Timetable:
    tid : int
    dep : str
    reg : str
    ac : str
    year : str
    sem : str
    sec : str
    week : str
    t1 : str
    t2 : str
    t3 : str
    t4 : str
    t5 : str
    t6 : str
    t7 : str

class Facultyload:
    lid : int
    fname : str
    dep : str
    week : str
    t1 : str
    t2 : str
    t3 : str
    t4 : str
    t5 : str
    t6 : str
    t7 : str