package hw2;


import java.io.*;
import java.util.Iterator;

import org.mindswap.pellet.jena.PelletReasonerFactory;




import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryExecution;
import com.hp.hpl.jena.query.QueryExecutionFactory;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.rdf.model.*;
import com.hp.hpl.jena.reasoner.Reasoner;
import com.hp.hpl.jena.reasoner.ReasonerRegistry;
import com.hp.hpl.jena.reasoner.ValidityReport;
import com.hp.hpl.jena.reasoner.rulesys.GenericRuleReasoner;
import com.hp.hpl.jena.reasoner.rulesys.Rule;
import com.hp.hpl.jena.util.FileManager;

public class OntologyAlignment {
	static String defaultNameSpace = "http://www.semanticweb.org/socialnetwork/linkin#";
	
	Model _travel = null;
	Model schema = null;
	InfModel inferredTravel = null;

	public static void main(String[] args) throws IOException {

		
		OntologyAlignment hello = new OntologyAlignment();
		
		
		//Load my FOAF friends
		System.out.println("Load Travel Ontology");
		hello.populateFOAFFriends();
		
		hello.populateFOAFSchema();
		
		
		//Run reasoner to  align the instances
		System.out.println("\nRun a Reasoner");
		hello.bindReasoner();
		//System.out.println("Running Pellet");
		//hello.runPellet();
		
		// Say Hello to myself
		System.out.println("\nQuery 1 Result: ");
		hello.query1(hello.inferredTravel); 
		
		System.out.println("\nQuery 2 Result: ");
		hello.query2(hello.inferredTravel);
		
		System.out.println("\nQuery 3 Result: ");
		hello.query3(hello.inferredTravel);
		
		System.out.println("\nQuery 4 Result: ");
		hello.query4(hello.inferredTravel);
		
		
		
		System.out.println("\nSuccess!");
	}
	

	
	private void populateFOAFFriends(){
		_travel = ModelFactory.createOntologyModel();
		InputStream inFoafInstance = FileManager.get().open("Ontologies/travel.owl");
		_travel.read(inFoafInstance,defaultNameSpace);
		//inFoafInstance.close();
	}
	
	private void query1(Model model){
		//Hello to Me - focused search
		runQuery2(" select DISTINCT ?x ?y where{ ?x travel:hasAccommodation ?y ."
				+ "?y travel:hasRating ?z . "
				+ "?z travel:hasNumericValue ?val "
				+ "filter(?val >= 3) .}", model);}  //add the query string}
	
	private void query2(Model model){
		//Hello to Me - focused search
		runQuery1(" select DISTINCT ?x where{ ?x travel:hasDemographic travel:Families ."
				+ "optional {?x travel:hasRating ?y .}"
				+ "optional {?x travel:hasActivity ?z .}}", model);}  //add the query string}
	
	private void query3(Model model){
		//Hello to Me - focused search
		runQuery1("SELECT ?x {?x travel:hasDemographic travel:ActivePeople .{?x travel:hasRating ?y . } UNION{?x travel:hasActivity ?z . } }", model);}  //add the query string}
	
	private void query4(Model model){
		//Hello to just my friends - navigation
		runQuery1("SELECT ?x {{?x travel:hasAccommodation ?w .}{?x travel:hasDemographic travel:SeniorCitizens .} UNION {?x travel:hasRating ?y .} OPTIONAL {?x travel:hasActivity ?z . } }", model);} //add the query string}
	
	
	private void populateFOAFSchema() throws IOException{
		InputStream inFoaf = FileManager.get().open("Ontologies/travel.owl");
		InputStream inFoaf2 = FileManager.get().open("Ontologies/travel.owl");
		schema = ModelFactory.createOntologyModel();
		//schema.read("http://xmlns.com/foaf/spec/index.rdf");
		//_travel.read("http://xmlns.com/foaf/spec/index.rdf");
		
		// Use local copy for demos without network connection
		schema.read(inFoaf, defaultNameSpace);
		_travel.read(inFoaf2, defaultNameSpace);	
		inFoaf.close();
		inFoaf2.close();
		}
	
	
	private void bindReasoner(){
	    Reasoner reasoner = ReasonerRegistry.getOWLReasoner();
	    reasoner = reasoner.bindSchema(schema);
	    inferredTravel = ModelFactory.createInfModel(reasoner, _travel);
	    
		Writer writer = null;
		try {
		    writer = new BufferedWriter(new OutputStreamWriter(
		          new FileOutputStream("Ontologies/inferredtravel.owl"), "utf-8"));
		    inferredTravel.write(writer);
		} catch (IOException ex) {
		  // report
		} finally {
		   try {writer.close();} catch (Exception ex) {}
		}

	}

	private void runQuery1(String queryRequest, Model model){
		
		StringBuffer queryStr = new StringBuffer();
		// Establish Prefixes
		//Set default Name space first
		queryStr.append("PREFIX people" + ": <" + defaultNameSpace + "> ");
		queryStr.append("PREFIX rdfs" + ": <" + "http://www.owl-ontologies.com/travel.owl#" + "> ");
		queryStr.append("PREFIX rdf" + ": <" + "http://www.owl-ontologies.com/travel.owl#" + "> ");
		queryStr.append("PREFIX travel" + ": <" + "http://www.owl-ontologies.com/travel.owl#" + "> ");
		
		//Now add query
		queryStr.append(queryRequest);
		Query query = QueryFactory.create(queryStr.toString());
		QueryExecution qexec = QueryExecutionFactory.create(query, model);
		try {
		ResultSet response = qexec.execSelect();
		
		while( response.hasNext()){
			QuerySolution soln = response.nextSolution();
			RDFNode name = soln.get("?x");
			if( name != null ){
				System.out.println(  name.toString() );
			}
			else
				System.out.println("No Reseult found!");
			}
		} finally { qexec.close();}				
		}
	
private void runQuery2(String queryRequest, Model model){
		
		StringBuffer queryStr = new StringBuffer();
		// Establish Prefixes
		//Set default Name space first
		queryStr.append("PREFIX people" + ": <" + defaultNameSpace + "> ");
		queryStr.append("PREFIX rdfs" + ": <" + "http://www.owl-ontologies.com/travel.owl#" + "> ");
		queryStr.append("PREFIX rdf" + ": <" + "http://www.owl-ontologies.com/travel.owl#" + "> ");
		queryStr.append("PREFIX travel" + ": <" + "http://www.owl-ontologies.com/travel.owl#" + "> ");
		
		//Now add query
		queryStr.append(queryRequest);
		Query query = QueryFactory.create(queryStr.toString());
		QueryExecution qexec = QueryExecutionFactory.create(query, model);
		try {
		ResultSet response = qexec.execSelect();
		
		while( response.hasNext()){
			QuerySolution soln = response.nextSolution();
			RDFNode name = soln.get("?x ?y");
			if( name != null ){
				System.out.println( name.toString() );
			}
			else
				System.out.println("No Result found!");
			}
		} finally { qexec.close();}				
		}
		
	
	private void runJenaRule(Model model){
		String rules = "[emailChange: (?person <http://xmlns.com/foaf/0.1/mbox> ?email), strConcat(?email, ?lit), regex( ?lit, '(.*@gmail.com)') -> (?person <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://org.semwebprogramming/chapter2/people#GmailPerson>)]";

		Reasoner ruleReasoner = new GenericRuleReasoner(Rule.parseRules(rules));
		ruleReasoner = ruleReasoner.bindSchema(schema);
	    inferredFriends = ModelFactory.createInfModel(ruleReasoner, model);	
	}
	
	private void runPellet( ){
		Reasoner reasoner = PelletReasonerFactory.theInstance().create();
	    reasoner = reasoner.bindSchema(schema);
	    inferredFriends = ModelFactory.createInfModel(reasoner, _travel);
	    
	    ValidityReport report = inferredFriends.validate();
	    //printIterator(report.getReports(), "Validation Results");
		
	}
    public static void printIterator(Iterator i, String header) {

        System.out.println(header);

        for(int c = 0; c < header.length(); c++)

            System.out.print("=");

        System.out.println();
       

        if(i.hasNext()) {

	        while (i.hasNext()) 

	            System.out.println( i.next() );

        }       

        else

            System.out.println("<EMPTY>");

        

        System.out.println();

    }

    public void setRestriction(Model model) throws IOException{
    	// Load restriction - if entered in model with reasoner, reasoner sets entailments
		InputStream inResInstance = FileManager.get().open("Ontologies/restriction.owl");
		model.read(inResInstance,defaultNameSpace);
		inResInstance.close();
		
		/*
		FileOutputStream outFoafInstance;
		try {
			outFoafInstance = new 
FileOutputStream("Ontologies/friendsWithRestriction.turtle");
			model.write(outFoafInstance, "TURTLE");
			outFoafInstance.close();
		} catch (Exception e) {
			 //TODO Auto-generated catch block
			e.printStackTrace();
		}
		*/	
    }
    
}