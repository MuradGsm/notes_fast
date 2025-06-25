from fastapi import FastAPI, HTTPException, status
import uvicorn 
from schemas import NoteIn, NoteOut
import stroage
from typing import List

app = FastAPI()


@app.post("/notes/add")
def add_notes(note: NoteIn):
    new_note = NoteOut(id = stroage.note_id_counter, title=note.title, content=note.content)
    stroage.notes_db[stroage.note_id_counter] = new_note
    stroage.note_id_counter += 1
    return new_note


@app.get('/notes', response_model=List[NoteOut])
def all_notess():
    return list(stroage.notes_db.values())


@app.get('/notes/{note_id}')
def note(note_id: int):
    for i in stroage.notes_db.keys():
        if i == note_id:
            return stroage.notes_db[i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')


@app.put("/notes/{note_id}", response_model=NoteOut)
def note_put(note_id: int, note: NoteIn):
    if note_id not in stroage.notes_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    updated_note = NoteOut(id=note_id, title=note.title, content=note.content)
    stroage.notes_db[note_id] = updated_note
    return updated_note
    
@app.delete('/notes/{note_id}')
def delete_note(note_id: int):
    if note_id not in stroage.notes_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Notes note found')
    del stroage.notes_db[note_id]
    return {'Message': 'Note deleted succesfully'}

if __name__ == '__main__':
    uvicorn.run(app, host = '0.0.0.0', port=8000)