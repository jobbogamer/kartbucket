
var newTrackID = -1;
var newPersonID = -1;

function prepareEditModal(trackID, trackName, personID, personName, character, kart, wheels, glider, choiceOfKart, allowsCustomisation)
{
    $("#edit-modal .modal-title").html("Add Time - " + trackName);

    $("#edit-modal-person-field").val(personID);

    $("#edit-modal-time-field").val("");
    $("#edit-modal-split1-field").val("");
    $("#edit-modal-split2-field").val("");
    $("#edit-modal-split3-field").val("");

    $("#edit-modal-character-field").val(character);
    $("#edit-modal-kart-field").val(kart);
    $("#edit-modal-wheels-field").val(wheels);
    $("#edit-modal-glider-field").val(glider);

    if (!allowsCustomisation)
    {
        $("#wheels-field").hide();
        $("#glider-field").hide();

        if (!choiceOfKart)
        {
            $("#kart-field").hide();
        }
    }

    newTrackID = trackID;
    newPersonID = personID;
}

function submitTime()
{

}
