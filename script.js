const el_filters = document.querySelectorAll('[name="year"], [name="type"], [name="event"]'),
  el_filterable = document.querySelectorAll('[data-filterable]');

const applyFilter = () => {

  // Filter checked inputs
  const el_checked = [...el_filters].filter(el => el.checked && el.value);

  // Collect checked inputs values to array
  const filters = [...el_checked].map(el => el.value);

  // Get elements to filter
  const el_filtered = [...el_filterable].filter(el => {
    const props = el.getAttribute('data-filterable').trim().split(/\s+/);
    return filters.every(fi => props.includes(fi))
  });

  // Hide all
  el_filterable.forEach(el => el.classList.add('is-hidden'));

  // Show filtered
  el_filtered.forEach(el => el.classList.remove('is-hidden'));
}

// Assign event listener
el_filters.forEach(el => el.addEventListener('change', applyFilter));
// Init
applyFilter()-;