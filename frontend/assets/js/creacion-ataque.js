function handle_response(response) {
    if (!response.ok) {
        throw new Error('Error al crear el ataque');
    }
    return response.json();
}

function handle_error(error) {
    console.log('Error: ', error);
    alert('error al enviar el formulario: ' + error.message);
}

function process_data(data){
    console.log("respuesta del servidor: ", data);
} 

function handle_submit(event) {
    event.preventDefault(); 
    const formData = new FormData(event.target);

    fetch('http://localhost:5000/nuevo_ataque', {
        method: 'POST',
        body: formData
    })
    .then(handle_response)
    .then(process_data)
    .catch(handle_error);
}