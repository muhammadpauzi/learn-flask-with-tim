async function deleteNote(id) {
    try {
        await fetch('/delete', {
            method: 'DELETE',
            body: JSON.stringify({ id }),
        });
        window.location.href = '/';
    } catch (err) {
        alert('Cannot delete note, please delete again leter.')
        console.error(err.message);
    }
}