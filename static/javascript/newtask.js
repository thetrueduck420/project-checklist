function newtask()
{
    const TaskName = document.getElementById("newtask").value
    const CheckList = document.getElementById("checklistinputdiv")

    const Task = document.createElement("input")
    const Label = document.createElement("h3")
    Task.type = "checkbox"
    Task.className = "checkbox"
    Task.name = TaskName + "__!NEW!__"
    Task.checked = true

    Label.innerText = "[ " + TaskName + " (will be unchecked upon confirmation.) "

    //CheckList.innerHTML += "<input type=\"checkbox\" class=\"checkbox\" name=\"" + TaskName + "\">"
    CheckList.appendChild(Task)
    CheckList.appendChild(Label)

    document.getElementById("newtask").value = ""
}