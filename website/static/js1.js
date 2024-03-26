// Function to update the slider value
function updateSliderValue(sliderId, value) {
    var displayValue = value;
  
    // Check if the slider is for distance or price
    if (sliderId === 'distance') {
      // Convert the value to kilometers
      displayValue = (parseFloat(value) * 0.1).toFixed(1) + ' KM';
    } else if (sliderId === 'price') {
      // Convert the value to Ukrainian Hryvnia (ГРН)
      displayValue = parseFloat(value) * 50 + ' ГРН';
    }
  
    // Update the span element with the current value
    var sliderValueElement = document.getElementById(sliderId + '-value');
    sliderValueElement.innerHTML = `<span>${sliderId.charAt(0).toUpperCase() + sliderId.slice(1)}:</span><br>${displayValue}`;
  }
  
  // Add event listeners to update the slider value when the page loads
  window.addEventListener('DOMContentLoaded', function () {
    // Get the initial values of the sliders
    var distanceSlider = document.getElementById('distance');
    var priceSlider = document.getElementById('price');
  
    // Update the initial slider values
    updateSliderValue('distance', distanceSlider.value);
    updateSliderValue('price', priceSlider.value);
  
    // Add event listeners to update the slider values when they change
    distanceSlider.addEventListener('input', function () {
      updateSliderValue('distance', this.value);
    });
  
    priceSlider.addEventListener('input', function () {
      updateSliderValue('price', this.value);
    });
  });
  