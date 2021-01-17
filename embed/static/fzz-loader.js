       /**
            * the FZ constructor
            *
            */
           class FZ {
            /**
             *
         */
            constructor(uri) {
                this.xml = undefined; // store the raw xml data
                this.filename = uri || ''; // store the fzz filename
                this.fritzingVersion = '';
                this.boards = []; // list of FZBoard items
                this.programs = {}; // list of FZProgram items
                this.instances = {}; //
                this.views = {}; //
            }

            /**
             * get the BOM
             */
            getBOM() {
                let bomData = [];
                for (let i = 0; i < this.fz.instances.length; i++) {
                    // console.log(this.fz.instances[i]);
                    if (this.fz.instances[i].moduleIdRef !== 'WireModuleID' && this.fz.instances[i].moduleIdRef !== 'LogoImageModuleID') {
                        let bomItem = {
                            moduleIdRef: this.fz.instances[i].moduleIdRef,
                            active: true,
                        };
                        bomData.push(bomItem);
                    }
                }
                return bomData;
            }
        }
   
        class FZBoard {
            /**
             * the FZBoard constructor
             */
            constructor() {
                this.moduleId = '';
                this.title = '';
                this.instance = '';
                this.width = '';
                this.height = '';
            }
        }

        class FZProgram {
            /**
             * the FZProgram constructor
             */
            constructor() {
                this.language = '';
                this.source = '';
            }
        }

        // parse fz xml data and return a FZ object.
        function parseFZ(filename, src, cb) {
                let tmpFZ = new FZ();
                tmpFZ.filename = filename;
                tmpFZ.xml = src;
                //console.log(src);
                var options = {
                    ignoreAttributes: false,
                    ignoreNameSpace: false,
                };
                var jsonobj = parser.parse(src, options);
                //console.log(jsonobj);
                if (jsonobj) {
                    tmpFZ.fritzingVersion = jsonobj.module["@_fritzingVersion"]
                    var tmpkeys = Object.keys(jsonobj.module);
                    //console.log(tmpkeys);
                    for (var i = 0; i < tmpkeys.length; i++) {
                        //console.log(tmpkeys[i]);
                        //
                        switch (tmpkeys[i]) {
                            case 'boards':
                                tmpFZ.boards = parseFZBoards(jsonobj.module.boards);
                                //console.log("End");
                                break;
                            //
                            case 'programs':
                                tmpFZ.programs = parseFZPrograms(jsonobj.module.programs);
                                break;
                            //
                            case 'views':
                                tmpFZ.views = parseFZViews(jsonobj.module.views);
                                break;
                            //
                            case 'instances':
                                tmpFZ.instances = parseFZInstances(jsonobj.module.instances);
                                break;
                            // 
                            default:
                                console.log(tmpkeys[i]);
                        }
                        // 
                    }
                
                }
                //console.log(tmpFZ);
                return tmpFZ;
                //cb(tmpFZZ);   
            } 
        function parseFZBoards(xml) {
            //console.log('parseFZBoards', xml);
            let tmpNodes = Object.keys(xml);
           // console.log('tmpNodes', tmpNodes);
            //console.log('BOARD', tmpNodes.length, tmpNodes);

            let tmpBoards = [];

            for (let j = 0; j < tmpNodes.length; j++) {
               // console.log(tmpNodes[j]);
                if (tmpNodes[j] === 'board') {
                    //console.log("here");
                    let tmpBoard = new FZBoard();

                    let tmpAttr = Object.keys(xml[tmpNodes[j]]);
                   // console.log(tmpAttr);
                    for (let a = 0; a < tmpAttr.length; a++) {
                       // console.log(tmpAttr[a]);
                        switch (tmpAttr[a]) {
                            case '@_moduleId':
                                tmpBoard.moduleId = xml.board["@_moduleId"];
                              //  console.log('tmpBoard.moduleId', tmpBoard.moduleId);
                                break;
                            case '@_title':
                                tmpBoard.title = xml.board["@_title"];
                                break;
                            case '@_instance':
                                tmpBoard.instance = xml.board["@_instance"];
                                break;
                            case '@_width':
                                // TODO: parse measurement
                                tmpBoard.width = xml.board["@_width"];
                                break;
                            case '@_height':
                                // TODO: parse measurement
                                tmpBoard.height = xml.board["@_height"];
                                break;
                            default:
                        }
                    }
                    
                    //console.log(tmpBoard.moduleId);
                    /* console.log(tmpAttr);
                    for (let a = 0; a < tmpAttr.length; a++) {
                        console.log(tmpAttr[a]);
                        switch (tmpAttr[a].name) {
                            case 'moduleId':
                                tmpBoard.moduleId = tmpAttr[a].nodeValue;
                                console.log('tmpBoard.moduleId', tmpBoard.moduleId);
                                break;
                            case 'title':
                                tmpBoard.title = tmpAttr[a].nodeValue;
                                break;
                            case 'instance':
                                tmpBoard.instance = tmpAttr[a].nodeValue;
                                break;
                            case 'width':
                                // TODO: parse measurement
                                tmpBoard.width = tmpAttr[a].nodeValue;
                                break;
                            case 'height':
                                // TODO: parse measurement
                                tmpBoard.height = tmpAttr[a].nodeValue;
                                break;
                            default:
                        }
                    } */
                    tmpBoards.push(tmpBoard);
                }
            }
            console.log('tmpBoards:', tmpBoards);
            return tmpBoards; 
        }

        function parseFZPrograms(xml) {
            // console.log('parseFZPrograms', xml);
            let programs = [];
            for (let i = 0; i < xml.childNodes.length; i++) {
                let tmpNode = xml.childNodes[i];
                // console.log('view', tmpNode);
                if (tmpNode.nodeName === 'program') {
                    // console.log(tmpNode);

                    let tmpProgram = new FZProgram();
                    tmpProgram.source = tmpNode.innerHTML;

                    for (let a = 0; a < tmpNode.attributes.length; a++) {
                        let tmpAttr = tmpNode.attributes[a];
                        switch (tmpAttr.name) {
                            case 'language':
                                tmpProgram.language = tmpAttr.nodeValue;
                                break;
                        }
                    }

                    programs.push(tmpProgram);
                }
            }
            return programs;
        }

        function parseFZViews(xml) {
            //console.log('parseFZViews', xml);
            let tmpNode = Object.keys(xml);
            //console.log('view', tmpNode);

            // the object we want to return
            let views = [];

            for (let i = 0; i < tmpNode.length; i++) {
                 
                if (tmpNode[i] === 'view') {
                    // console.log('attributes', tmpNode.attributes);

                    // the view data we push to the views variable
                   
                    let innertmpkeys = xml[tmpNode[i]];
                    for (let a = 0; a < Object.keys(innertmpkeys).length; a++) {
                        let tmpView = {
                            name: '',
                            backgroundColor: '',
                            gridSize: '',
                            showGrid: true,
                            alignToGrid: true,
                            viewFromBelow: false,
                            gpgKeepout: '',
                            autorouteViaHoleSize: '',
                            autorouteTraceWidth: '',
                            autorouteViaRingThickness: '',
                            drcKeepout: '',
                        };
                        let tmpAttr = innertmpkeys[a];
                        //console.log(tmpAttr);
                        let tmpkeys = Object.keys(tmpAttr);
                        for (let b = 0; b < tmpkeys.length; b++) {
                            //console.log(tmpkeys[b]);
                            switch (tmpkeys[b]) {
                                case '@_name':
                                    tmpView.name = tmpAttr["@_name"];
                                    //console.log(tmpView.name);
                                    break;

                                case '@_backgroundColor':
                                    tmpView.backgroundColor = tmpAttr["@_backgroundColor"];
                                    break;

                                case '@_gridSize':
                                    tmpView.gridSize = tmpAttr["@_gridSize"];
                                    break;

                                case '@_showGrid':
                                    tmpView.showGrid =  tmpAttr["@_showGrid"];
                                    break;

                                case '@_alignToGrid':
                                    tmpView.alignToGrid =  tmpAttr["@_alignToGrid"];
                                    break;

                                case '@_viewFromBelow':
                                    tmpView.viewFromBelow = tmpAttr["@_viewFromBelow"];
                                    break;

                            }

                        }
                        //console.log(views);
                        views.push(tmpView);
                        //console.log("tmpView:", tmpView);
                        
                    }
                    
                    
                }
                
            }
            //console.log(views);
            return views;
        }

        function parseFZInstances(xml) {
                //console.log('parseFZInstances', xml);
                let tmpNode = Object.keys(xml);
                //console.log('view', tmpNode);

                let instances = [];

                for (let i = 0; i < tmpNode.length; i++) {


                    if (tmpNode[i] === 'instance') {
                        // console.log(tmpNode);


                        let innertmpkeys = xml[tmpNode[i]];
                        // get the attributes of the instance tag...
                        //console.log('attributes', innertmpkeys);
                        for (let a = 0; a < Object.keys(innertmpkeys).length; a++) {
                            let tmpInstance = {
                                moduleIdRef: '',
                                modelIndex: '',
                                path: '',
                                property: {
                                    name: '',
                                    value: '',
                                },
                                title: '',
                                views: {
                                    breadboardView: undefined,
                                    pcbView: undefined,
                                    schematicView: undefined,
                                },
                            };
                            let tmpAttr = innertmpkeys[a];
                            //console.log(tmpAttr);
                            let tmpkeys = Object.keys(tmpAttr);
                            //console.log(tmpkeys);
                            for (let b = 0; b < tmpkeys.length; b++) {

                                switch (tmpkeys[b]) {
                                    case '@_moduleIdRef':
                                        tmpInstance.moduleIdRef = tmpAttr["@_moduleIdRef"];
                                        //console.log(tmpInstance.moduleIdRef);
                                        break;
                                    case '@_modelIndex':
                                        tmpInstance.modelIndex = tmpAttr["@_modelIndex"];
                                        break;
                                    case '@_path':
                                        tmpInstance.path = tmpAttr["@_path"];
                                        break;
                                }
                            }
                            let property = [];
                            for (let j = 0; j < Object.keys(tmpAttr).length; j++) {
                                let tmpkey = Object.keys(tmpAttr);
                                //console.log('--', j, tmpkey);

                                switch (tmpkey[j]) {
                                    // get property...
                                    case 'property':
                                        var tmpProp = tmpAttr['property'];
                                        //console.log('tmpProp:', tmpProp);
                                        // get attributes...
                                        for (let pa = 0; pa < tmpProp.length; pa++) {
                                            let tmppropvalues = tmpProp[pa];
                                            //console.log(tmppropvalues);
                                            let tmpProperty = {
                                                name: '',
                                                value: '',
                                            };
                                            let tmppropkeys = Object.keys(tmppropvalues);
                                            //console.log(tmppropkeys);
                                            for (let pv = 0; pv < tmppropkeys.length; pv++) {
                                                let propvalue = tmppropkeys[pv];
                                                //console.log(propvalue);
                                                switch (propvalue) {
                                                    case '@_name':
                                                        tmpProperty.name = tmpProp[pa]['@_name'];
                                                        //console.log(tmpInstance.property.name);
                                                        break;
                                                    case '@_value':
                                                        tmpProperty.value = tmpProp[pa]['@_value'];
                                                        break;
                                                }


                                            }
                                            property.push(tmpProperty);


                                        }
                                        //console.log(property);
                                        tmpInstance.property = property;
                                        break;

                                    // get title...
                                    case 'title':
                                        // console.log('TITLE', tmpNode.childNodes[j].innerHTML);
                                        tmpInstance.title = tmpAttr["title"];
                                        break;

                                    // get views...
                                    case 'views':
                                        tmpInstance.views = parseFZInstancesViews(tmpAttr["views"]);
                                        break;

                                }

                            }
                            //console.log(tmpInstance);
                            //instances.push(tmpInstance);


                            //console.log(tmpInstance);
                            instances.push(tmpInstance);
                        }

                    }
                }
                console.log(instances);
                return instances;
            }

        function parseFZInstancesViews(xml) {
            //console.log('call parseFZInstancesViews', xml);
            let tmpViews = {
                breadboardView: undefined,
                pcbView: undefined,
                schematicView: undefined,
            };
            let tmpkeys = Object.keys(xml);
            //console.log(tmpkeys);

            for (var i = 0; i < tmpkeys.length; i++) {
                
                let tmpInstanceView = {
                    layer: '',
                    geometry: {
                        x: 0,
                        y: 0,
                        z: 0,
                    },
                    connectors: [],
                };
                switch (tmpkeys[i]) {
                    case 'breadboardView':
                        let tmpNode = xml[tmpkeys[i]];
                        //console.log('BB', tmpNode);
                        let nodeName = Object.keys(tmpNode);
                        //console.log(nodeName);
                        tmpInstanceView.layer = tmpkeys[i];
                        for (let ib = 0; ib < nodeName.length; ib++) {
                            
                            switch (nodeName[ib]) {
                                case 'geometry':
                                    let innerkeys = Object.keys(tmpNode[nodeName[ib]]);
                                    //console.log('X', 'Y', innerkeys);
                                    let tmpAttr = tmpNode[nodeName[ib]];
                                    //console.log(tmpAttr);
                                    for (var i = 0; i < innerkeys.length; i++) {
                                        //console.log(innerkeys[i]);
                                        switch (innerkeys[i]) {
                                            case '@_x':
                                                tmpInstanceView.geometry.x = tmpAttr['@_x'];
                                                //console.log(tmpAttr['@_x']);
                                                break;
                                            case '@_y':
                                                tmpInstanceView.geometry.y = tmpAttr['@_y'];
                                                break;
                                            case '@_z':
                                                tmpInstanceView.geometry.z = tmpAttr['@_z'];
                                                break;
                                        }
                                    }
                                    break;

                                /* case 'connectors':
                                    var tmpCons = tmpNode.childNodes[ib].childNodes;
                                    // console.log(tmpCons);
                                    for (let ic = 0; ic < tmpCons.length; ic++) {
                                        switch (tmpCons[ic].nodeName) {
                                            case 'connector':
                                                // console.log('CON', tmpCons[ic]);

                                                break;
                                            default:
                                        }
                                    }
                                    break; */
                            }
                        }
                        tmpViews.breadboardView = tmpInstanceView;

                        break;
                }
            }


            return tmpViews;
        }

        class FZZ {
            /**
             * The FZZ constructor
             * @param {Object} opt constructor options
             * @param {Object} opt.uri name of the fzz (zip archive) file
             * @param {Object} opt.zip the list of files contained at the fzz archive
             * @param {Object} opt.files
             * @param {Object} opt.fz
             * @param {Object} opt.code
             * @param {Object} opt.parts
             */
            constructor(opt) {
                opt = opt || {};
                this.uri = opt.uri || undefined;
                this.zip = opt.zip || undefined;
                this.files = opt.files || [];
                this.fz = opt.fz || new FZ();
                // this.code = opt.code || new FZZCode();
                this.parts = opt.parts || []; // list of parts (fzp and svg files)
            }
        }