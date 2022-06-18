from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def get_object_or_error(Model, pk):
    try:
        return Model.objects.get(id=pk)
    except Model.DoesNotExist:
        return HttpResponse("ERROR 404!!")

@login_required(login_url='login')
def edit(request, pk, Model, name_redirect, path, NameForm):
    item = get_object_or_error(Model, pk)
    
    if item.user == request.user:
        form = NameForm(instance=item)

        if request.method == 'POST':
            form = NameForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                
                if name_redirect == 'home':
                    return redirect('home')
                else:
                    return redirect(name_redirect, pk=item.todo_list.id)

    else:
        return HttpResponse("ERROR 404!!")
    
    return render(request, path, {'form': form, 'item': item})