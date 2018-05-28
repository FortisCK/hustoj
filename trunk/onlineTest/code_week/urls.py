from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^course_list/$', course_list_for_student, name='course_list_for_student'),
    url(r'^courses/$', course_list_for_teacher, name='course_list_for_teacher'),
    url(r'^add_course/$', add_course, name='add_codeweek_course'),
    url(r'^course-(?P<courseId>\d+)/$', view_course, name='view_course_for_teacher'),
    url(r'^course_(?P<courseId>\d+)/$', student_view_course, name='view_course_for_student'),
    url(r'^sheji_problem_list/', list_sheji, name='sheji_problem_list'),
    url(r'^del-sheji/$', delete_sheji, name='del_sheji'),
    url(r'^sheji-detail-$',ShejiProblemDetailView.as_view(),name='_sheji_problem_detail'),
    url(r'^update-sheji-$', update_sheji, name='_update_sheji'),
    url(r'^sheji-detail-(?P<pk>\d+)/$',ShejiProblemDetailView.as_view(),name='sheji_detail'),
    url(r'^update-sheji-(?P<id>\d*)/$', update_sheji, name='update_sheji'),
    url(r'^add-sheji', add_sheji, name='add_sheji'),
    url(r'^get-sheji/$', get_json_sheji, name='get_json_sheji'),
    url(r'^get-problem-student-(?P<id>\d+)/$', get_problem_student, name='get_problem_student'),
    url(r'^download-(?P<courseId>\d+)/$', download, name='download_file'),
    url(r'^download-problem-(?P<problemId>\d+)/$', download_problem, name='download_problem_file'),
    url(r'^student-info-(?P<courseId>\d+)/$', student_info, name='student_info'),
    url(r'^teacher_update/$', teacher_update_info, name='teacher_update_course'),
    url(r'^teacher-info-(?P<courseId>\d+)/$', teacher_course_info, name='teacher_course_info'),
    url(r'^get-select-problem-(?P<courseId>\d+)/$', get_select_problem, name='get_select_problem'),
    url(r'^remove-select-problem/$', remove_select_problem, name='remove_select_problem'),
    url(r'^add-problem-student-(?P<courseId>\d+)/$', add_problem_student, name='add_problem_student'),
    url(r'^get-student-state-(?P<courseId>\d+)/$', get_student_state, name='get_student_state'),
    url(r'^remove-student/$', remove_student, name='remove_student'),
    url(r'^choose-problem-(?P<courseId>\d+)/$', choose_problem, name='choose_problem'),
    url(r'^submit-code-(?P<courseId>\d+)/$', submit_code, name='submit_code'),
    url(r'^get-code-(?P<fileId>\d+)/$', get_code_file, name='get_code'),
    url(r'^get-all-history-(?P<courseId>\d+)/$', get_all_code_history, name='get_all_code_history'),
    url(r'^get-code-zip-(?P<historyId>\d+)/$', download_codeZip, name='get_code_zip'),
    url(r'^teacher-student-info-(?P<courseId>\d+)/$', teacher_get_student_info, name='teacher_get_student_info'),
    url(r'^teacher-code-zip-(?P<courseId>\d+)-(?P<historyId>\d+)/$', teacher_get_code_zip, name='teacher_get_code_zip'),
    url(r'^teacher-single-code-(?P<courseId>\d+)-(?P<fileId>\d+)/$', teacher_get_single_code, name='teacher_get_single_code'),
    url(r'^teacher-all-history-(?P<courseId>\d+)-(?P<groupId>\d+)/$', teacher_get_all_code_history, name='teacher_get_all_history'),
    url(r'^teacher-read-code-(?P<courseId>\d+)-(?P<groupId>\d+)-(\d+)/$', teacher_read_code, name='teacher_read_code'),
    url(r'^teacher-check-student/$', teacher_check_student, name='teacher_check_student'),
    url(r'^teacher-download-(?P<problemId>\d+)/$', teacher_download, name='teacher_download_descfile'),
    url(r'^get-all-report-(?P<courseId>\d+)/$', get_all_report_history, name='get_all_report_history'),
    url(r'^upload-report-(?P<courseId>\d+)/$', handle_upload_report, name='upload_report'),
    url(r'^download-report-(?P<historyId>\d+)/$', download_report, name='get_report'),
    url(r'^teacher-get-all-report-history-(?P<courseId>\d+)-(?P<groupId>\d+)/$', teacher_get_all_report_history, name='teacher_get_all_report_history'),
    url(r'^teacher-download-report-(?P<courseId>\d+)-(?P<historyId>\d+)/$', teacher_download_report, name='teacher_download_report'),
    url(r'^teacher-tar-request-(?P<courseId>\d+)/', handelTeacherTar, name='teacher_tar_request'),
    url(r'^teacher-download-tar-(?P<courseId>\d+)/', teacherDownloadTar, name='teacher_download_tar'),
    url(r'^course-latest-info-(?P<courseId>\d+)/', teacherViewLatestInfo, name='teacher_latest_info'),
    url(r'^teacher-get-latest-info-(?P<courseId>\d+)', teacherGetLatestInfo, name='teacher_get_latest_info'),
    url(r'^teacher-get-contribution-(?P<groupId>\d+)', teacherGetContribution, name='teacher_get_contribution'),
]