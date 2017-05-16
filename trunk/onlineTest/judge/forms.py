from django import forms
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from judge.models import Problem, ClassName, KnowledgePoint2, ChoiceProblem, TiankongProblem, GaicuoProblem


class ProblemAddForm(forms.Form):
    title = forms.CharField(label='标题', widget=forms.TextInput(
        attrs={'class': 'form-control', 'data-validation': 'required', 'data-validation-error-msg': "请输入题目标题"}))
    description = forms.CharField(label='题目描述', widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '3', 'data-validation': 'required',
               'data-validation-error-msg': "请输入题目描述"}))
    input = forms.CharField(label='输入描述', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                            required=False)
    output = forms.CharField(label='输出描述', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                             required=False)
    sample_input1 = forms.CharField(label='样例输入1', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                                    required=False)
    sample_output1 = forms.CharField(label='样例输出1', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                                     required=False)
    sample_input2 = forms.CharField(label='样例输入2', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                                    required=False)
    sample_output2 = forms.CharField(label='样例输出2', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                                     required=False)
    time_limit = forms.IntegerField(label='时间限制', widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'number', 'aria-describedby': 'basic-addon2'}), initial=1)
    memory_limit = forms.IntegerField(label='内存限制', widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'number', 'aria-describedby': 'basic-addon2'}), initial=128)
    classname = forms.ModelChoiceField(label='所属课程', queryset=ClassName.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    keypoint = forms.CharField(label='知识点，请从下面的下拉菜单中选择添加', widget=forms.TextInput(
        attrs={'type': 'hidden', 'data-validation': 'required', 'data-validation-error-msg': "请输入题目标题"}))

    def save(self, user, problemid=None):
        cd = self.cleaned_data
        title = cd['title']
        description = cd['description']
        input = cd['input']
        output = cd['output']
        sample_input1 = cd['sample_input1']
        sample_output1 = cd['sample_output1']
        sample_input2 = cd['sample_input2']
        sample_output2 = cd['sample_output2']
        time_limit = cd['time_limit']
        memory_limit = cd['memory_limit']
        keypoint = cd['keypoint'].split(',')
        if problemid:
            problem = Problem.objects.get(pk=problemid)
            problem.title = title
            problem.description = description
            problem.time_limit = time_limit
            problem.memory_limit = memory_limit
            problem.input = input
            problem.output = output
            problem.sample_input = sample_input1
            problem.sample_output = sample_output1
            problem.sample_input2 = sample_input2
            problem.sample_output2 = sample_output2
            problem.creater = user
            problem.knowledgePoint1.clear()
            problem.knowledgePoint1.clear()
        else:
            id=get_problemid()
            problem = Problem(
                problem_id=id,
                title=title,
                description=description,
                time_limit=time_limit,
                memory_limit=memory_limit,
                input=input,
                output=output,
                sample_input=sample_input1,
                sample_output=sample_output1,
                sample_input2=sample_input2,
                sample_output2=sample_output2,
                creater=user
            )
        problem.save()
        for point in keypoint:
            problem.knowledgePoint2.add(KnowledgePoint2.objects.get(pk=point))
        for point in problem.knowledgePoint2.all():
            problem.knowledgePoint1.add(point.upperPoint)
        for point in problem.knowledgePoint1.all():
            problem.classname.add(point.classname)
        problem.save()
        return problem


class ChoiceAddForm(forms.Form):
    CHOICES = (('a', 'A',), ('b', 'B',), ('c', 'C'), ('d', 'D'))
    title = forms.CharField(label='题干', widget=forms.Textarea(
        attrs={'class': 'form-control', 'required': 'required'}))
    a = forms.CharField(max_length=200, widget=forms.Textarea(
        attrs={'class': 'form-control', 'required': 'required', 'rows': '3'}))
    b = forms.CharField(max_length=200, widget=forms.Textarea(
        attrs={'class': 'form-control', 'required': 'required', 'rows': '3'}))
    c = forms.CharField(max_length=200, widget=forms.Textarea(
        attrs={'class': 'form-control', 'required': 'required', 'rows': '3'}))
    d = forms.CharField(max_length=200, widget=forms.Textarea(
        attrs={'class': 'form-control', 'required': 'required', 'rows': '3'}))
    selection = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)

    classname = forms.ModelChoiceField(label='所属课程', queryset=ClassName.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    keypoint = forms.CharField(label='知识点，请从下面的下拉菜单中选择添加', widget=forms.TextInput(
        attrs={'type': 'hidden', 'data-validation': 'required', 'data-validation-error-msg': "请输入题目标题"}))

    def save(self, user, id=None):
        cd = self.cleaned_data
        keypoint = cd['keypoint'].split(',')
        if id:
            with transaction.atomic():
                choiceProblem = ChoiceProblem.objects.select_for_update().get(pk=id)
                choiceProblem.c = cd['c']
                choiceProblem.title = cd['title']
                choiceProblem.a = cd['a']
                choiceProblem.b = cd['b']
                choiceProblem.d = cd['d']
                choiceProblem.right_answer = cd['selection']
                choiceProblem.creater = user
                choiceProblem.classname.clear()
                choiceProblem.knowledgePoint1.clear()
                choiceProblem.save()
        else:
            choiceProblem = ChoiceProblem(title=cd['title'], a=cd['a'], b=cd['b'], c=cd['c'], d=cd['d'],
                                          right_answer=cd['selection'], creater=user)
            choiceProblem.save()
        for point in keypoint:
            choiceProblem.knowledgePoint2.add(KnowledgePoint2.objects.get(pk=point))
        for point in choiceProblem.knowledgePoint2.all():
            choiceProblem.knowledgePoint1.add(point.upperPoint)
        for point in choiceProblem.knowledgePoint1.all():
            choiceProblem.classname.add(point.classname)
        choiceProblem.save()
        return choiceProblem

class GaicuoProblemAddForm(forms.Form):
    title = forms.CharField(label='标题', widget=forms.TextInput(
        attrs={'class': 'form-control', 'data-validation': 'required', 'data-validation-error-msg': "请输入题目标题"}))
    description = forms.CharField(label='题目描述', widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '3', 'data-validation': 'required',
               'data-validation-error-msg': "请输入题目描述"}))
    input = forms.CharField(label='输入描述', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                            required=False)
    output = forms.CharField(label='输出描述', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                             required=False)
    program = forms.CharField(label='程序代码', widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '20',"spellcheck":"false",
               'placeholder': '示例：\n#include<stdio.h>\nint main(){\n  int a,b;\n  /*---------found-------*/\n  scanf(%d,%d,a,b);\n  sum=a+b;\n  /*---------found-------*/\n  return 0;\n}'}),
                              required=False)
    sample_input1 = forms.CharField(label='样例输入1', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                                    required=False)
    sample_output1 = forms.CharField(label='样例输出1', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                                     required=False)
    sample_input2 = forms.CharField(label='样例输入2', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                                    required=False)
    sample_output2 = forms.CharField(label='样例输出2', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                                     required=False)
    time_limit = forms.IntegerField(label='时间限制', widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'number', 'aria-describedby': 'basic-addon2'}), initial=1)
    memory_limit = forms.IntegerField(label='内存限制', widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'number', 'aria-describedby': 'basic-addon2'}), initial=128)
    classname = forms.ModelChoiceField(label='所属课程', queryset=ClassName.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    keypoint = forms.CharField(label='知识点，请从下面的下拉菜单中选择添加', widget=forms.TextInput(
        attrs={'type': 'hidden', 'data-validation': 'required', 'data-validation-error-msg': "请输入题目标题"}))

    def save(self, user, problemid=None):
        cd = self.cleaned_data
        title = cd['title']
        description = cd['description']
        input = cd['input']
        output = cd['output']
        program = cd['program']
        sample_input1 = cd['sample_input1']
        sample_output1 = cd['sample_output1']
        sample_input2 = cd['sample_input2']
        sample_output2 = cd['sample_output2']
        time_limit = cd['time_limit']
        memory_limit = cd['memory_limit']
        keypoint = cd['keypoint'].split(',')
        if problemid:
            problem = GaicuoProblem.objects.get(pk=problemid)
            problem.title = title
            problem.description = description
            problem.time_limit = time_limit
            problem.memory_limit = memory_limit
            problem.input = input
            problem.output = output
            problem.program = program
            problem.sample_input = sample_input1
            problem.sample_output = sample_output1
            problem.sample_input2 = sample_input2
            problem.sample_output2 = sample_output2
            problem.creater = user
            problem.knowledgePoint1.clear()
            problem.knowledgePoint1.clear()
        else:
            id=get_problemid()
            problem = GaicuoProblem(
                problem_id=id,
                title=title,
                description=description,
                time_limit=time_limit,
                memory_limit=memory_limit,
                input=input,
                output=output,
                program=program,
                sample_input=sample_input1,
                sample_output=sample_output1,
                sample_input2=sample_input2,
                sample_output2=sample_output2,
                creater=user
            )
        problem.save()
        for point in keypoint:
            problem.knowledgePoint2.add(KnowledgePoint2.objects.get(pk=point))
        for point in problem.knowledgePoint2.all():
            problem.knowledgePoint1.add(point.upperPoint)
        for point in problem.knowledgePoint1.all():
            problem.classname.add(point.classname)
        problem.save()
        return problem

class TiankongProblemAddForm(forms.Form):
    title = forms.CharField(label='标题', widget=forms.TextInput(
        attrs={'class': 'form-control', 'data-validation': 'required', 'data-validation-error-msg': "请输入题目标题"}))
    description = forms.CharField(label='题目描述', widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '3', 'data-validation': 'required',
               'data-validation-error-msg': "请输入题目描述"}))
    input = forms.CharField(label='输入描述', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                            required=False)
    output = forms.CharField(label='输出描述', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                             required=False)
    program = forms.CharField(label='程序代码', widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '20', "spellcheck": "false",
               "placeholder": "示例：\n#include<stdio.h>\nint fun(int,int);\nint main(){\n  int a,b;\n  scanf(\"%d,%d\",a,b); \n  sum=a+b;\n  return 0;\n}\n//请在下面填写你的答案\nint fun(int,int)"}),
                              required=False)
    sample_input1 = forms.CharField(label='样例输入1', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                                    required=False)
    sample_output1 = forms.CharField(label='样例输出1', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                                     required=False)
    sample_input2 = forms.CharField(label='样例输入2', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                                    required=False)
    sample_output2 = forms.CharField(label='样例输出2', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
                                     required=False)
    time_limit = forms.IntegerField(label='时间限制', widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'number', 'aria-describedby': 'basic-addon2'}), initial=1)
    memory_limit = forms.IntegerField(label='内存限制', widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'number', 'aria-describedby': 'basic-addon2'}), initial=128)
    classname = forms.ModelChoiceField(label='所属课程', queryset=ClassName.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    keypoint = forms.CharField(label='知识点，请从下面的下拉菜单中选择添加', widget=forms.TextInput(
        attrs={'type': 'hidden', 'data-validation': 'required', 'data-validation-error-msg': "请输入题目标题"}))

    def save(self, user, problemid=None):
        cd = self.cleaned_data
        title = cd['title']
        description = cd['description']
        input = cd['input']
        output = cd['output']
        program = cd['program']
        sample_input1 = cd['sample_input1']
        sample_output1 = cd['sample_output1']
        sample_input2 = cd['sample_input2']
        sample_output2 = cd['sample_output2']
        time_limit = cd['time_limit']
        memory_limit = cd['memory_limit']
        keypoint = cd['keypoint'].split(',')
        if problemid:
            problem = TiankongProblem.objects.get(pk=problemid)
            problem.title = title
            problem.description = description
            problem.time_limit = time_limit
            problem.memory_limit = memory_limit
            problem.input = input
            problem.output = output
            problem.program = program
            problem.sample_input = sample_input1
            problem.sample_output = sample_output1
            problem.sample_input2 = sample_input2
            problem.sample_output2 = sample_output2
            problem.creater = user
            problem.knowledgePoint1.clear()
            problem.knowledgePoint1.clear()
        else:
            id=get_problemid()
            problem = TiankongProblem(
                problem_id=id,
                title=title,
                description=description,
                time_limit=time_limit,
                memory_limit=memory_limit,
                input=input,
                output=output,
                program=program,
                sample_input=sample_input1,
                sample_output=sample_output1,
                sample_input2=sample_input2,
                sample_output2=sample_output2,
                creater=user
            )
        problem.save()
        for point in keypoint:
            problem.knowledgePoint2.add(KnowledgePoint2.objects.get(pk=point))
        for point in problem.knowledgePoint2.all():
            problem.knowledgePoint1.add(point.upperPoint)
        for point in problem.knowledgePoint1.all():
            problem.classname.add(point.classname)
        problem.save()
        return problem

def get_problemid():
    max=0

    try:
        problem_max = Problem.objects.order_by('-problem_id')[0:1].get()
        if problem_max.problem_id>max :
            max=problem_max.problem_id
    except ObjectDoesNotExist:
        pass

    try:
        tiankong_max = TiankongProblem.objects.order_by('-problem_id')[0:1].get()
        if tiankong_max.problem_id>max :
            max=tiankong_max.problem_id
    except ObjectDoesNotExist:
        pass

    try:
        gaicuo_max = GaicuoProblem.objects.order_by('-problem_id')[0:1].get()
        if gaicuo_max.problem_id>max :
            max=gaicuo_max.problem_id
    except ObjectDoesNotExist:
        pass

    max=max+1
    return max
