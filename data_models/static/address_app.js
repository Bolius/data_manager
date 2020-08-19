const url_parts = window.location.href.split("/");
dawaAutocomplete.dawaAutocomplete(
  document.getElementById("autocomplete-input"),
  {
    select: function(selected) {
      console.log("Selected address:");
      console.log("YO:");
      let url = `${url_parts[0]}//${url_parts[2]}/${selected["data"]["id"]}/`;
      console.log(url)
    }
  }
);
