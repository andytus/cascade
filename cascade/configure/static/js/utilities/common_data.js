/**
 *
 * User: jbennett
 * Date: 4/5/13
 * Time: 12:46 PM
 *
 */


(function (cartlogic) {

    function streetSuffix(){
     var self = this;
       self.suffix = {suffix: ['ALLEY','ANEX','ARCADE','AVENUE','BAYOU','BEACH','BEND','BLUFF','BLUFFS','BOTTOM','BOULEVARD','BRANCH','BRIDGE','BROOK','BROOKS','BURG','BURGS','BYPASS','CAMP','CANYON','CAPE','CAUSEWAY','CENTER','CENTERS','CIRCLE','CIRCLES','CLIFF','CLIFFS','CLUB','COMMON','COMMONS','CORNER','CORNERS','COURSE','COURT','COURTS','COVE','COVES','CREEK','CRESCENT','CREST','CROSSING','CROSSROAD','CROSSROADS','CURVE','DALE','DAM','DIVIDE','DRIVE','DRIVES','ESTATE','ESTATES','EXPRESSWAY','EXTENSION','EXTENSIONS','FALL','FALLS','FERRY','FIELD','FIELDS','FLAT','FLATS','FORD','FORDS','FOREST','FORGE','FORGES','FORK','FORKS','FORT','FREEWAY','GARDEN','GARDENS','GATEWAY','GLEN','GLENS','GREEN','GREENS','GROVE','GROVES','HARBOR','HARBORS','HAVEN','HEIGHTS','HIGHWAY','HILL','HILLS','HOLLOW','INLET','ISLAND','ISLANDS','ISLE','JUNCTION','JUNCTIONS','KEY','KEYS','KNOLL','KNOLLS','LAKE','LAKES','LAND','LANDING','LANE','LIGHT','LIGHTS','LOAF','LOCK','LOCKS','LODGE','LOOP','MALL','MANOR','MANORS','MEADOW','MEADOWS','MEWS','MILL','MILLS','MISSION','MOTORWAY','MOUNT','MOUNTAIN','MOUNTAINS','NECK','ORCHARD','OVAL','OVERPASS','PARK','PARKS','PARKWAY','PARKWAYS','PASS','PASSAGE','PATH','PIKE','PINE','PINES','PLACE','PLAIN','PLAINS','PLAZA','POINT','POINTS','PORT','PORTS','PRAIRIE','RADIAL','RAMP','RANCH','RAPID','RAPIDS','REST','RIDGE','RIDGES','RIVER','ROAD','ROADS','ROUTE','ROW','RUE','RUN','SHOAL','SHOALS','SHORE','SHORES','SKYWAY','SPRING','SPRINGS','SPUR','SPURS','SQUARE','SQUARES','STATION','STRAVENUE','STREAM','STREET','STREETS','SUMMIT','TERRACE','THROUGHWAY','TRACE','TRACK','TRAFFICWAY','TRAIL','TRAILER','TUNNEL','TURNPIKE','UNDERPASS','UNION','UNIONS','VALLEY','VALLEYS','VIADUCT','VIEW','VIEWS','VILLAGE','VILLAGES','VILLE','VISTA','WALK','WALKS','WALL','WAY','WAYS','WELL','WELLS'],
                     abbv: ['ALY','ANX','ARC','AVE','BYU','BCH','BND','BLF','BLFS','BTM','BLVD','BR','BRG','BRK','BRKS','BG','BGS','BYP','CP','CYN','CPE','CSWY','CTR','CTRS','CIR','CIRS','CLF','CLFS','CLB','CMN','CMNS','COR','CORS','CRSE','CT','CTS','CV','CVS','CRK','CRES','CRST','XING','XRD','XRDS','CURV','DL','DM','DV','DR','DRS','EST','ESTS','EXPY','EXT','EXTS','FALL','FLS','FRY','FLD','FLDS','FLT','FLTS','FRD','FRDS','FRST','FRG','FRGS','FRK','FRKS','FT','FWY','GDN','GDNS','GTWY','GLN','GLNS','GRN','GRNS','GRV','GRVS','HBR','HBRS','HVN','HTS','HWY','HL','HLS','HOLW','INLT','IS','ISS','ISLE','JCT','JCTS','KY','KYS','KNL','KNLS','LK','LKS','LAND','LNDG','LN','LGT','LGTS','LF','LCK','LCKS','LDG','LOOP','MALL','MNR','MNRS','MDW','MDWS','MEWS','ML','MLS','MSN','MTWY','MT','MTN','MTNS','NCK','ORCH','OVAL','OPAS','PARK','PARK','PKWY','PKWY','PASS','PSGE','PATH','PIKE','PNE','PNES','PL','PLN','PLNS','PLZ','PT','PTS','PRT','PRTS','PR','RADL','RAMP','RNCH','RPD','RPDS','RST','RDG','RDGS','RIV','RD','RDS','RTE','ROW','RUE','RUN','SHL','SHLS','SHR','SHRS','SKWY','SPG','SPGS','SPUR','SPUR','SQ','SQS','STA','STRA','STRM','ST','STS','SMT','TER','TRWY','TRCE','TRAK','TRFY','TRL','TRLR','TUNL','TPKE','UPAS','UN','UNS','VLY','VLYS','VIA','VW','VWS','VLG','VLGS','VL','VIS','WALK','WALK','WALL','WAY','WAYS','WL','WLS']}

      self.get_abbreviated= function(){
            return self.suffix.abbv
        }

    }
  cartlogic.streetSuffix = streetSuffix;
}
   )(window.cartlogic);





        self.getTypeOptions = function () {
            url = cart_type_options_api_url + "?format=jsonp&callback=?";
            data = {'size':self.cart().cart_type__size()};
            $.getJSON(url, data, function (data) {
                var cartTypeOptions = $.map(data, function (item) {
                    return new cartlogic.TypeOption(item)
                });
                self.cart_type_options(cartTypeOptions);
                //Set drop down to current cart type
                $("#cart-info-edit-type option[value='" + self.cart().cart_type__id() + "']").attr("selected", "selected");
            })
        };