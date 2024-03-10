document.addEventListener('DOMContentLoaded', function () {
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
    const server = 'http://localhost:5000'
    // Event listener for starting the Python script
    startButton.addEventListener('click', function () {
        console.log('startButton')
        var cellphone = document.getElementById('cellphone').value;

           fetch(server+'/start-script', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ cellphone: cellphone })
            })
            .then(response => {
                if (response.ok) {
                    console.log('Python script started successfully');
                } else {
                    console.error('Failed to start Python script');
                }
            })
            .catch(error => console.error('Error:', error));
    });

    // Event listener for stopping the Python script
    stopButton.addEventListener('click', function () {
          console.log('stopButton');
          fetch(server + '/stop-script')
            .then(response => {
                if (response.ok) {
                    console.log('Python script stopped successfully');
                } else {
                    console.error('Failed to stop Python script');
                }
            })
            .catch(error => console.error('Error:', error));
    });
});