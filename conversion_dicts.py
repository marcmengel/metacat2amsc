

amsctype2mctype_dict = {
   "scientificWork": "dataset",
   "artifactCollection": "dataset"
   "artifact": "file",
   "mlmodel": "file",
   "table": "file",
   "reference": "file",
}

amsctype2omtype_dict = {
   "scientificWork": "Collection",
   "artifactCollection": "Collection"
   "artifact": "File",
   "mlmodel": "mlModel",
   "table": "Table",
   "reference": "file",
}

meta2open_dict = {
 "id": "FQN",
 "name": "Name",
 "owner": "owners",
 "size": "size",
 "datasets": "ParentFQN",
 "updated_by": "updatedBy",
 "updated_timestamp": "updatedAt",
 "AmSC.Algorithm": "algorithm",
 "AmSC.Columns": "columns",
 "AmSC.Dashboard": "dashboard",
 "AmSC.DisplayName": "displayName",
 "AmSC.Domains": "domains",
 "AmSC.Extension": "extension",
 "AmSC.Features": "mlFeatures",
 "AmSC.Format", "fileFormat"
 "AmSC.Hyperparameters": "mlHyperParameters",
 "AmSC.License": "license",
 "AmSC.Location": "sourceURL", 
 "AmSC.ModelVersion": "modelVersion",
 "AmSC.OriginalSource": "originalSource",
 "AmSC.PID": "PID",
 "AmSC.ReferenceType": "type",
 "AmSC.RelationshipType": "relationshipTy-e",
 "AmSC.ServerEndpoint": "server",
 "AmSC.ServiceType": "serviceType",
 "AmSC.SourceEntity": "",
 "AmSC.StorageLocation": "mlStore",
 "AmSC.TableType": "tableType",
 "AmSC.Tags": "tags",
 "AmSC.TargetURI", "href",
 "AmSC.TargetVariable": "target",
 "AmSC.Type": "type",
}

open2meta_dict = { v: k for k,v in meta2open_dict.items() }
