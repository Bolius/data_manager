function fetch_bbr_data(id) {
  const url = window.location.href
    .split("/")
    .slice(0, 3)
    .join("/");

   query = `
        query getBBR($dawaId: String!) {
            address(dawaId: $dawaId) {
                house{
                    address
                    buldings {
                        id
                        constructionYear
                        reconstructionYear
                        buildingArea
                        groundArea
                        garageArea
                        carportArea
                        outhouseArea
                        roofArea
                        commercialArea
                        otherArea
                        numFloors
                        numBaths
                        numToilets
                        numRooms
                        residentialType
                        energyType
                        heatInstall
                        heatType
                        heatSupply
                        waterSupply
                        wallMaterial
                        roofingMaterial
                        propertyType
                        kitchenFacility
                        toiletFacility
                        bathingFacility
                    }
                }
            }
        }`;

  return fetch(`${url}/graphql/`, {
    method: "POST",
    headers: {
      "content-type": "application/json"
    },
    body: JSON.stringify({
      query,
      variables: { dawaId: "40eb1f85-9c53-4581-e044-0003ba298018" }
    })
  })
    .then(res => res.json())
    .catch(err => {
      console.error(err);
    });
}


function insertBbrData(data){
    const house = data["address"]["house"]
    document.getElementById('address').textContent = house.address
    document.getElementById('BBR').textContent = JSON.stringify(house.buldings[0], null, '\t')
}
