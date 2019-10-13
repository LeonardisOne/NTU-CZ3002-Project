import math, random
from .models import ChapterTeam, Student

def create_teams(chapter, alr_started):
    if alr_started==False and chapter.can_start==True:
        print('creating')#debug
        students=chapter.module.student_set.all()
        num_students = len(students)
        num_teams = math.ceil(num_students/5)
        print(num_teams)#debug
        print(num_students % 5)#debug
        team_no = 1
        team_list = []
        while num_teams > 0:
            team_created = ChapterTeam.objects.create_team(chapter, 'Team ' + str(team_no))
            team_list.append(team_created)
            team_no += 1
            num_teams -= 1
        
        #team_list = ChapterTeam.objects.filter(chapter=chapter)
        print(team_list)#debug

        for team in team_list:
            students_inside = random.sample(list(students), min(5, num_students))

            for student in students_inside:
                student.joined_teams.add(team)
                students = students.exclude(pk=student.pk)
            
            num_students -= min(5, num_students)

        return team_list
        #debug statements
        """ a1 = ChapterTeam.objects.get(team_name = 'Team 1', chapter=chapter)
        print(a1.student_set.all()) """
    else:
        print('cannot create teams')#debug
        return []