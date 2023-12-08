function performSearch() {
  const searchZip = document.getElementById('searchInput').value;
  if (!searchZip) {
    alert('Please enter a zip code.');
    return;
  }
  if (searchZip.length !== 5 || isNaN(searchZip)) {
    alert('Please enter a valid 5-digit zip code.');
    return;
  }

  // Redirect to results.html with search query as URL parameter
  window.location.href = `results.html?search=${searchZip}`;
}

document.addEventListener('DOMContentLoaded', function () {
  const searchParams = new URLSearchParams(window.location.search);
  const searchZip = searchParams.get('search');

  if (!searchZip) {
    console.error('Error: search query not found in URL parameter.');
    return;
  }

  fetch('daycares.json')
    .then(response => response.json())
    .then(daycares => {
      const results = daycares.filter(daycare => daycare.zip === searchZip);

      const searchResultsDiv = document.getElementById('searchResults');
      if (!searchResultsDiv) {
        console.error('Error: searchResults div not found.');
        return;
      }

      searchResultsDiv.innerHTML = '';

      if (results.length === 0) {
        searchResultsDiv.innerHTML = 'No daycares found for the provided zip code.';
      } else {
        // Show search results with zip code in heading
      const heading = document.createElement('h1');
      heading.textContent = `Search Results for ${searchZip}`;
      searchResultsDiv.appendChild(heading);

        results.forEach(result => {
          const resultDiv = document.createElement('div');
          resultDiv.classList.add('result-container');
          resultDiv.innerHTML = `<strong>${result.name}</strong> (${result.rating}) <br> ${result.description} <br> ${result.contact_number}`;
          searchResultsDiv.appendChild(resultDiv);
        });
      }
    })
    .catch(error => {
      console.error('Error fetching daycares:', error);
    });
}); 
