function confirmdelete(Name)
{
    const Confirm = confirm('Are you sure you want to delete ' + Name + ' ? You will not be able to recover it.')

    if (Confirm)
    {
        window.location.href = "/Projects/delete/" + Name
    }
}