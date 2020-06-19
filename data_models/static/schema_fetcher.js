function schemaFetcher() {
  const schemaQuery = JSON.stringify({
    query: `{
      house: __type(name: "House"){
        fields{
          name
          type {
            ofType{
              name
              description
              fields {name
                description
                type {
                  kind
                  ofType {
                    kind
                    name
                    description
                    fields {
                      name
                      description
                    }
                  }
                }
              }
            }
          }
        }
      }
    }`
  });
  const url_parts = window.location.href.split("/");
  this.url = `${url_parts[0]}//${url_parts[2]}/graphql/`;
  return fetch(this.url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: schemaQuery
  }).then(resp => resp.json());
}

function schemaToQuery(schema) {
  const rootFields = schema["data"]["house"]["fields"].filter(
    field => !field.name.toLowerCase().includes("input")
  );

  this.app.schema = [
    parseRootField(rootFields[0]),
    parseRootField(rootFields[1])
  ];

  return {
    query: `{house(kvhxInput: "<KVHX>"){
       ${this.app.schema.map(field => buildQuery(field))}
     }
  `.replace(",", "\n ")
  };
}

async function constructQuery() {
  const schema = await schemaFetcher();
  this.app.query = schemaToQuery(schema);
}

async function fetchData(kvhx) {
  let bod = { query: this.app.query.query.replace("<KVHX>", kvhx) };
  bod = JSON.stringify(bod);
  console.log(bod);
  const resp = await fetch(this.url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: bod
  });
  const houseData = await resp;
  console.log(houseData);
  this.app.houseData = houseData["data"]["house"]; //.data.house;
  this.app.loading = false;
  return houseData;
}

function parseRootField(root) {
  let schema = {
    label: root.name,
    description: root.type.ofType.description
  };
  if (root.type.ofType.fields.length > 0) {
    schema["children"] = parseChildren(root.type.ofType.fields);
  }
  return schema;
}

function parseChildren(children) {
  console.log(children);
  let ans = [];
  for (var child of children) {
    let field = {
      label: child.name,
      description:
        child.description !== null
          ? child.description
          : child.type.ofType.description
    };
    if (child.type !== undefined && child.type.ofType.fields !== null) {
      field["children"] = parseChildren(child.type.ofType.fields);
    } else {
      field["children"] = [];
    }
    ans.push(field);
  }
  return ans;
}

// TODO FINISH THIS
function buildQuery(field) {
  console.log("IN build");
  console.log(field);
  if (field.children.length > 0) {
    return `${field.label} {
      ${field.children
        .reduce((acc, child) => buildQuery(child) + acc, "")
        .toString()
        .replace(",", " ")}
    }`;
  } else {
    return `${field.label}\n`;
  }
}
