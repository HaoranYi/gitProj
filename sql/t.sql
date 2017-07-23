SELECT T.name as TName, T.rate as Rate, S.name as SName, S.age as Age, S.grade as Grade,
    C.starttime as StartTime, C.endtime as EndTime
FROM tbClass C
JOIN tbTeacher T ON C.teacher_id = T.id
JOIN tbStudent S ON C.student_id = S.id

