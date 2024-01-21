function startLoadAnimation() {
  const button = document.getElementById('btn-analyze');
  button.disabled = true;
  button.innerHTML = 'Loading...'
}

function stopLoadAnimation(text='Analyze') {
  const button = document.getElementById('btn-analyze');
  button.innerHTML = text;
  button.disabled = false;
}

function analyze() {
  const text = document.getElementsByTagName('textarea')[0].value;
  const result = document.getElementById('result');
  result.hidden = true;
  startLoadAnimation();
  fetch('/api/analyze', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({'text': text})
  })
  .then(response => response.json())
  .then(body => {
    refreshHistory();
    stopLoadAnimation();
    const labels =  (body.labels.length > 0) ? body.labels.join(', ') : 'none'
    result.innerText = `Labels: ${labels}. Comment: ${body.comment}`;
    result.hidden = false;
  })
  .catch(error => {
    stopLoadAnimation('Errored out. Repeat analysis');
    result.hidden = true;
    console.error('Error:', error);
  });
}

function reset() {
  stopLoadAnimation();
  document.getElementsByTagName('textarea')[0].value = '';
  const result = document.getElementById('result');
  result.innerText = '';
  result.hidden = true;
}

function createHistoryItem(labels, text) {
  // Create label
  const label = document.createElement('label');
  label.className = 'field';
  // Create textarea
  const textarea = document.createElement('textarea');
  textarea.disabled = true;
  textarea.className = 'fs-small';
  textarea.style.minHeight = '0';
  textarea.textContent = text;
  // Create span
  const span = document.createElement('span');
  span.className = 'label';
  span.textContent = `labels: ${(labels.length > 0) ? labels.join(', ') : 'none'}`;
  // Append & return
  label.appendChild(textarea);
  label.appendChild(span);
  return label
}

function refreshHistory() {
  const history = document.getElementById('history');
  fetch('/api/history', {
    method: 'GET'
  })
  .then(response => response.json())
  .then(records => {
    // Remove existing elements
    while (history.firstChild) {
      history.removeChild(history.lastChild);
    }
    // Append records.
    records.forEach((record) => {
      const item = createHistoryItem(record.labels, record.text);
      history.appendChild(item);
    });
    // Add placeholder.
    if (history.childElementCount === 0) {
      const p = document.createElement('p');
      p.classList.add('fs-small');
      p.innerText = 'Nothing but crickets...';
      history.appendChild(p);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

window.onload = function () {
  refreshHistory();
}
