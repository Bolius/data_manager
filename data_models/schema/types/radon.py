import graphene
import requests


class RadonResp(graphene.ObjectType):
    riskClass = graphene.Int()
    classificationText = graphene.String()
    becquerel = graphene.Float()
    header = graphene.String()
    text = graphene.String()


def bbrToRadon(data):
    (bbr, house) = data
    form_fields = {
        "zip": house.zip_code,
        "has_basement": 0 if bbr.basement_area == 0 else 1,
        "floors": bbr.num_floors,
        "kommune_id": house.municipality.admin_code,
        "build_year": bbr.construction_year,
        "rebuild_year": 0
        if bbr.reconstruction_year is None
        else bbr.reconstruction_year,
        "area_resi": bbr.building_area,
        "area_basement": bbr.basement_area,
        "rooms": bbr.num_rooms,
    }
    # Non uniform encoding for area_resi, booooh.
    resi_type = bbr.residential_type
    if resi_type == "130" or resi_type == "131":
        resi_type = "row"
    elif resi_type == "120":
        resi_type = "one_fam"
    elif resi_type == 140:
        resi_type = "story"
    elif resi_type == "multi":
        resi_type = "multi"  # One type cat matches
    else:
        resi_type = "oth"
    form_fields["resityp_geo"] = resi_type

    encoded_form = "&".join([f"{key}={form_fields[key]}" for key in form_fields])
    resp = requests.request(
        "POST",
        "http://radon:8888",
        data=encoded_form,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if resp.status_code != 200:
        print(resp.status_code)
        print(resp.content)
        raise ValueError("Invalid radon response")

    return RadonResponse(resp.json(), bbr, house)


def RadonResponse(data, bbr, house):
    riskClass = data["class"]
    classificationText = [
        "den laveste",
        "den næstlaveste",
        "den midderste",
        "den næsthøjeste",
        "den højeste",
    ][data["class"]]

    header = "Dit hjem estimeres til at have lav risiko for radon"
    if riskClass == 2 or riskClass == 3:
        header = "Dit hjem estimeres til at have middel risiko for radon"
    if riskClass == 4:
        header = "Dit hjem estimeres til at have høj risiko for radon"
    text = f"""<div>
        <p>
        Dit hus ligger i {house.municipality.name} Kommune, som i 2001 fik tildelt
        radonklasse 1, der er den næstlaveste risikoklasse. I denne risikoklasse
        er det vurderet, at 0.3-1% af alle boliger i kommunen har et radonniveau
        over 200 Bq/m<sup>3</sup>, hvor du som boligejer bør lave effektive
        foranstaltninger for at nedbringe niveauet.</p>
    """
    if bbr.residential_type in ["story", "140"]:
        text += """
        <p>Da du bor i lejlighed, er din risiko dog begrænset, da undersøgelser
        peger på, at radon ikke udgør et større problem i etageejendomme.</p>
        """
    text += """
      <p>
        Den eneste måde du finder ud af, hvor meget radon der er i dit hjem,
        er ved at teste for det.
       </p>
    </div>"""
    return RadonResp(
        riskClass=riskClass,
        classificationText=classificationText,
        becquerel=data["becquerel"],
        header=header,
        text=text,
    )
