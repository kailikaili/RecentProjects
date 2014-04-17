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
	
	Model _friends = null;
	Model schema = null;
	InfModel inferredFriends = null;

	public static void main(String[] args) throws IOException {

		
		OntologyAlignment hello = new OntologyAlignment();
		
		//Load my FOAF friends
		System.out.println("Load my FOAF Friends");
		hello.populateFOAFFriends();
		
		// Say Hello to myself
		System.out.println("\nMy name is Tom! Now my status is: ");
		hello.mySelf(hello._friends); 
		System.out.println("My Activities on Linkin are: ");
		hello.myActivity(hello._friends);
		System.out.println("My Background on Linkin are: ");
		hello.myBackground(hello._friends);
		
		// Say Hello to my FOAF Friends
		System.out.println("\nSay Hello to my Linkin Friends");
		hello.myFriends(hello._friends);
		
		//Add my new friends
		System.out.println("\nadd my new friends from FaceBook ");
		hello.populateNewFriends();
		
		//Say hello to my friends - hey my new ones are missing?
		System.out.println("\nSay hello to all my friends - hey friends from FaceBook are missing!");
		hello.myFriends(hello._friends);
		
		// Add the ontologies
		System.out.println("\nAdd the Ontologies");
		hello.populateFOAFSchema();
		hello.populateNewFriendsSchema();
		
		//See if the ontologies help identify my new friends? Nope!
		System.out.println("\nSee if the ontologies help to say hello to all my friends - Nope!");
		hello.myFriends(hello._friends);
		
		//Align the ontologies to bind my friends together
		System.out.println("\nOk, lets add alignment statements for the two ontologies.");
		hello.addAlignment();
		
		//Now say hello to my friends - nope still no new friends!
		System.out.println("\nTry again - Hello to all my friends - nope still not all!");
		hello.myFriends(hello._friends);
		
		//Run reasoner to  align the instances
		System.out.println("\nRun a Reasoner");
		hello.bindReasoner();
		//System.out.println("Running Pellet");
		//hello.runPellet();
		
		//Say hello to all my friends
		System.out.println("\fFinally- Hello to all my friends!");
		hello.myFriends(hello.inferredFriends);
		
		System.out.println("\nMy name is Tom! My information from two profiles : ");
		System.out.println("My Whole Activities are: ");
		hello.myActivity(hello.inferredFriends);
		System.out.println("My Whole Background are: ");
		hello.myFBackground(hello.inferredFriends);
	
		
		System.out.println("\nSuccess!");
	}
	

	
	private void populateFOAFFriends(){
		_friends = ModelFactory.createOntologyModel();
		InputStream inFoafInstance = FileManager.get().open("Ontologies/linkin.rdf");
		_friends.read(inFoafInstance,defaultNameSpace);
		//inFoafInstance.close();

	}
	
	private void mySelf(Model model){
		//Hello to Me - focused search
		runQuery(" select DISTINCT ?name where{ people:Tom foaf:has_status ?name}", model);}  //add the query string}
	
	private void myActivity(Model model){
		//Hello to Me - focused search
		runQuery(" select DISTINCT ?name where{ people:Tom foaf:has_activity ?name}", model);}  //add the query string}
	
	private void myBackground(Model model){
		//Hello to Me - focused search
		runQuery(" select DISTINCT ?name where{ people:Tom foaf:has_backgrounf ?name}", model);}  //add the query string}
	
	private void myFriends(Model model){
		//Hello to just my friends - navigation
		runQuery(" select DISTINCT  ?name where{  people:Tom foaf:has_connection ?name } ", model);} //add the query string}
	private void myFBackground(Model model){
		//Hello to Me - focused search
		runQuery(" select DISTINCT ?name where{ rdf:Tom rdf:has_about ?name}", model);}  //add the query string}
	
	
	

	
	
	
	private void populateNewFriends() throws IOException {		
		InputStream inFoafInstance = FileManager.get().open("Ontologies/facebook.rdf");
		_friends.read(inFoafInstance,defaultNameSpace);
		inFoafInstance.close();


	} 
	
	private void addAlignment(){
		
		// State that :individual is equivalentClass of foaf:Person
		Resource resource = schema.createResource(defaultNameSpace + "Name");
		Property prop = schema.createProperty("http://www.w3.org/2002/07/owl#equivalentClass");
		Resource obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#Person");
		schema.add(resource,prop,obj);
		
		// State that :individual is equivalentClass of foaf:Person
		resource = schema.createResource(defaultNameSpace + "Background");
		prop = schema.createProperty("http://www.w3.org/2002/07/owl#subClassOf");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#About");
		schema.add(resource,prop,obj);
		
		// State that :individual is equivalentClass of foaf:Person
		resource = schema.createResource(defaultNameSpace + "ContactInfo");
		prop = schema.createProperty("http://www.w3.org/2002/07/owl#subClassOf");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#About");
		schema.add(resource,prop,obj);

		// State that :individual is equivalentClass of foaf:Person
		resource = schema.createResource(defaultNameSpace + "Status");
		prop = schema.createProperty("http://www.w3.org/2002/07/owl#subClassOf");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#About");
		schema.add(resource,prop,obj);
		
		// State that :individual is equivalentClass of foaf:Person
		resource = schema.createResource(defaultNameSpace + "Activity");
		prop = schema.createProperty("http://www.w3.org/2002/07/owl#subClassOf");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#Affair");
		schema.add(obj,prop,resource);
		
		// State that :individual is equivalentClass of foaf:Person
		resource = schema.createResource(defaultNameSpace + "Activity");
		prop = schema.createProperty("http://www.w3.org/2002/07/owl#subClassOf");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#Movie");
		schema.add(obj,prop,resource);
		
		// State that :individual is equivalentClass of foaf:Person
		resource = schema.createResource(defaultNameSpace + "Activity");
		prop = schema.createProperty("http://www.w3.org/2002/07/owl#subClassOf");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#Music");
		schema.add(obj,prop,resource);
	
		
		//###############################################
		resource = schema.createResource(defaultNameSpace + "has_connection");
		//prop = schema.createProperty("http://www.w3.org/2000/01/rdf-schema#subPropertyOf");
		prop = schema.createProperty("http://www.w3.org/2002/07/owl#equivalentProperty");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#has_friends");
		schema.add(resource,prop,obj);
		
		//State that :hasFriend is a subproperty of foaf:knows
		resource = schema.createResource(defaultNameSpace + "has_background");
		prop = schema.createProperty("http://www.w3.org/2000/01/rdf-schema#subPropertyOf");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#has_about");
		schema.add(resource,prop,obj);
				
		//State that :hasFriend is a subproperty of foaf:knows
		resource = schema.createResource(defaultNameSpace + "has_contact");
		prop = schema.createProperty("http://www.w3.org/2000/01/rdf-schema#subPropertyOf");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#has_about");
		schema.add(resource,prop,obj);
		
		//State that :hasFriend is a subproperty of foaf:knows
		resource = schema.createResource(defaultNameSpace + "has_status");
		prop = schema.createProperty("http://www.w3.org/2000/01/rdf-schema#subPropertyOf");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#has_about");
		schema.add(resource,prop,obj);
		
		//State that :hasFriend is a subproperty of foaf:knows
		resource = schema.createResource(defaultNameSpace + "has_activity");
		prop = schema.createProperty("http://www.w3.org/2000/01/rdf-schema#subPropertyOf");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#has_Affair");
		schema.add(obj,prop,resource);
		
		//State that :hasFriend is a subproperty of foaf:knows
		resource = schema.createResource(defaultNameSpace + "has_activity");
		prop = schema.createProperty("http://www.w3.org/2000/01/rdf-schema#subPropertyOf");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#has_movie");
		schema.add(obj,prop,resource);
		
		//State that :hasFriend is a subproperty of foaf:knows
		resource = schema.createResource(defaultNameSpace + "has_activity");
		prop = schema.createProperty("http://www.w3.org/2000/01/rdf-schema#subPropertyOf");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#has_music");
		schema.add(obj,prop,resource);
		
		
		//State that sem web is the same person as Semantic Web
		resource = schema.createResource("http://www.semanticweb.org/socialnetwork/linkin#Tom");
		prop = schema.createProperty("http://www.w3.org/2002/07/owl#sameAs");
		obj = schema.createResource("http://www.semanticweb.org/socialnetwork/facebook#Tom");
		schema.add(resource,prop,obj);
		
		//String fileName = "E:/13Fall/SemanticWeb/hw2/AlignedOntology.rdf";
		//StringWriter out = new StringWriter();
		Writer writer = null;
		try {
		    writer = new BufferedWriter(new OutputStreamWriter(
		          new FileOutputStream("Ontologies/AlignedOntology.owl"), "utf-8"));
		    _friends.write(writer);
		} catch (IOException ex) {
		  // report
		} finally {
		   try {writer.close();} catch (Exception ex) {}
		}


	}
	
	private void populateFOAFSchema() throws IOException{
		InputStream inFoaf = FileManager.get().open("Ontologies/linkin.rdf");
		InputStream inFoaf2 = FileManager.get().open("Ontologies/linkin.rdf");
		schema = ModelFactory.createOntologyModel();
		//schema.read("http://xmlns.com/foaf/spec/index.rdf");
		//_friends.read("http://xmlns.com/foaf/spec/index.rdf");
		
		// Use local copy for demos without network connection
		schema.read(inFoaf, defaultNameSpace);
		_friends.read(inFoaf2, defaultNameSpace);	
		inFoaf.close();
		inFoaf2.close();
		}
	
	private void populateNewFriendsSchema() throws IOException {
		InputStream inFoafInstance = FileManager.get().open("Ontologies/facebook.rdf");
		_friends.read(inFoafInstance,defaultNameSpace);
		inFoafInstance.close();
	}
	
	private void bindReasoner(){
	    Reasoner reasoner = ReasonerRegistry.getOWLReasoner();
	    reasoner = reasoner.bindSchema(schema);
	    inferredFriends = ModelFactory.createInfModel(reasoner, _friends);
	    
		Writer writer = null;
		try {
		    writer = new BufferedWriter(new OutputStreamWriter(
		          new FileOutputStream("Ontologies/inferredAlignedOntology.owl"), "utf-8"));
		    inferredFriends.write(writer);
		} catch (IOException ex) {
		  // report
		} finally {
		   try {writer.close();} catch (Exception ex) {}
		}

	}

	private void runQuery(String queryRequest, Model model){
		
		StringBuffer queryStr = new StringBuffer();
		// Establish Prefixes
		//Set default Name space first
		queryStr.append("PREFIX people" + ": <" + defaultNameSpace + "> ");
		queryStr.append("PREFIX rdfs" + ": <" + "http://www.semanticweb.org/socialnetwork/linkin#" + "> ");
		queryStr.append("PREFIX rdf" + ": <" + "http://www.semanticweb.org/socialnetwork/facebook#" + "> ");
		queryStr.append("PREFIX foaf" + ": <" + "http://www.semanticweb.org/socialnetwork/linkin#" + "> ");
		
		//Now add query
		queryStr.append(queryRequest);
		Query query = QueryFactory.create(queryStr.toString());
		QueryExecution qexec = QueryExecutionFactory.create(query, model);
		try {
		ResultSet response = qexec.execSelect();
		
		while( response.hasNext()){
			QuerySolution soln = response.nextSolution();
			RDFNode name = soln.get("?name");
			if( name != null ){
				System.out.println( "Hello to " + name.toString() );
			}
			else
				System.out.println("No Friends found!");
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
	    inferredFriends = ModelFactory.createInfModel(reasoner, _friends);
	    
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
    
    public void myEmailFriends(Model model){
     	//just get all my email friends only - ones with email
		runQuery(" select DISTINCT ?name where{  ?sub rdf:type <http://org.semwebprogramming/chapter2/people#EmailPerson> . ?sub foaf:name ?name } ", model);  //add the query string

    }
    
    public void myGmailFriends(Model model){
		runQuery(" select DISTINCT ?name where{  ?sub rdf:type people:GmailPerson. ?sub foaf:name ?name } ", model);  //add the query string
   	
    }
}