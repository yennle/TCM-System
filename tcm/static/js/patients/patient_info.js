$(function(){
    var patient_id;
    var load_patient_modal = function(){
        $.ajax({
            type: "get",
            url: "{{url_for('patient_info', patient_id=patient.id)}}",
            dataType: "json",
            beforeSend:function(){
                $('#PatientModal').modal('show')
                // $('#patient_'+patient_id).modal('show')
            },
            success: function (response) {
                
            }
        });
    }
    // Binding
    $('#select_patient').on('click',load_patient_modal);
});

$.each(patient,function(i){
    id=patient[i][0]
    name=patient[i][1]
    dob=patient[i][2]
    gender=patient[i][3]
    phone=patient[i][4]
    $('#patient_'+id).modal("show");
  }) 
  $.each(row,function(key,value){
    patient_id=$(value).attr("data-id")
    alert('id:'+patient_id)
  })