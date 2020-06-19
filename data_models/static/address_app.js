dawaAutocomplete.dawaAutocomplete(
  document.getElementById("autocomplete-input"),
  {
    select: function(selected) {
      console.log("Selected address:");
      console.dir(selected);
    }
  }
);

var app = new Vue({
  delimiters: ["[[", "]]"],
  el: "#app",
  data: {
    url: "no url",
    fields: [],
    temp: "",
    noAddress: true,
    address: "",
    loading: true,
    houseData: { empty: true }
  },
  created: function() {
    constructQuery();
  },
  methods: {
    setAddress: function(dawa_obj) {
      this.address = dawa_obj.tekst;
      this.noAddress = false;
      const getSchema = async dawa_obj => {
        const kvhx = fetch(dawa_obj.data.href).then(resp => resp.json());

        const resp = await Promise.all([kvhx]).then(responses => {
          const kvhx = responses[0].kvhx;
          return kvhx;
        });
        return resp;
      };
      console.log("Resp is");
      getSchema(dawa_obj).then(kvhx => fetchData(kvhx));
    }
  }
});
