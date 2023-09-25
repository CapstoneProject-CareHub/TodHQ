function findStore() {
    const zipcode = document.getElementById('zipcode').value;
    if(!zipcode) {
        alert('Please enter a zip code.');
        return;
    }

    // Fetch store data. For simplicity, we're using dummy data
    const stores = [{
        name: "Daycare A",
        zip: "12345",
        address: "123 A Street"
    }, {
        name: "Daycare B",
        zip: "67890",
        address: "678 B Street"
    }];

    const results = stores.filter(store => store.zip === zipcode);
    
    const resultsDiv = document.getElementById('storeResults');
    resultsDiv.innerHTML = '';

    if(results.length === 0) {
        resultsDiv.innerHTML = 'No stores found for the provided zip code.';
    } else {
        results.forEach(result => {
            resultsDiv.innerHTML += `<div>${result.name} - ${result.address}</div>`;
        });
    }
}
