package group;

import field.AbstractField;
import field.Rational;
import field.TwoCycle;
import homomorphism.AbstractMatrix;
import homomorphism.GroupHomo;

import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.Map.Entry;

import util.Function;
import util.Tuple;
/**
 * The symmetric group class <tt>S_n</tt>: the set of all bijections of a finite
 * set onto itself. 
 * @author adin
 *
 * @param <X> the type of the underlying space (note any finite non-empty set becomes
 * a module of the symmetric group via the action described by each permutation 
 */
public class SymmetricGroup<X extends Object> extends AbstractNAG<SymmetricGroup<X>>implements Function<Tuple<X>,Tuple<X>> {
	/**the sign map: maps each permutation to its sign (zero if even, one if odd number of transpositions)*/
	public static final Sign<Object> SIGN = new Sign<Object>();
	/**the current argument*/
	private Tuple<X> arg;
	/**the current image value*/
	private Tuple<X> val;
	/**the ordered set of all disjoint cycles*/
	private TreeSet<Cycle> cycleMap;
	/**the greatest element in all cycles*/
	private int maxArg;
	/**
	 * Constructs the empty permutation - the identity
	 */
	public SymmetricGroup (){
		super();
		cycleMap = new TreeSet<Cycle> ();
	}
	/**
	 * Constructs a permutation specified by the argument array's entries
	 * The following convention applies:
	 * <ol>
	 * <li>if <code>cycleArray[i]!=cycleArray[i+1]</code> returns true for some indices <tt>i</tt>
	 * this permutation will contain a cycle of the form <tt>(..,cycleArray[i],cycleArray[i+1],..)</tt></li>
	 * <li>all repetitions are omitted - so, for example:
	 * <br /> <code>new SymmetricGroup&ltObject&gt (new int[]{0,0,0,1,2,0}).equals(new SymmetricGroup&ltObject&gt(new int[]{0,1,2}))</code>
	 * returns true
	 * </ol>
	 * @param cycleArray an array of integers
	 */
	public SymmetricGroup (int[] cycleArray){
		this();
		decomposeCycleArray(cycleArray);
	}
	/**
	 * Constructs a permutation based on the argument array <tt>cycleArray</tt>
	 *  of some arbitrary class <code>X</code>.
	 *  The following convention applies:
	 * <ol>
	 * <li>if <code>cycleArray[i].equals(cycleArray[i+1])</code> returns false for some indices <tt>i</tt>
	 * this permutation will contain a cycle of the form <tt>(..,cycleArray[i],cycleArray[i+1],..)</tt></li>
	 * <li>all repetitions are omitted - so, for example:
	 * <br /> <code>Object o1 = new Object(), o2 = new Object(), o3 = new Object();</code>
	 * <br />...
	 * <br /><code>new SymmetricGroup&ltObject&gt (new Object[]{o1,o1,o1,o2,o3,o1}).equals(new SymmetricGroup&ltObject&gt(new Object[]{o1,o2,o3}))</code>
	 * returns true
	 * </ol>
	 * This implies that any permutation cannot have more than <code>cycleArray.length</code> entries
	 * @param cycleArray an array of arbitrary type
	 */
	public SymmetricGroup (X[] cycleArray){
		this();
		decomposeCycleArray(cycleArray);
	}
	/**
	 * Constructs a permutation based on a single 
	 * cycle of length <code>cycle.length()</tt>
	 * @param cycle the cycle
	 */
	public SymmetricGroup (Cycle cycle){
		this();
		if(cycle.isClosed()) cycleMap.add(cycle);
		setMaxArg();
	}
	/**
	 * Constructs a new permutation by copying the
	 * argument permutation <tt>another</tt>
	 * @param another the permutation to copy
	 */
	public SymmetricGroup (SymmetricGroup<X> another) {
		this();
		for (Cycle cycle:another.cycleMap) cycleMap.add(new Cycle(cycle));
		setMaxArg();
	}
	/**
	 * Returns a square permutation matrix object representing
	 * this permutation
	 * @param one some non-zero element
	 * @param dim the dimension
	 * @return the permutation matrix
	 * @throws IllegalArgumentException if <code>one.isZero()</code> or <code>dim &lt getMaxArg()</code> returns
	 * true 
	 */
	public <F extends AbstractField<F>> AbstractMatrix<F> constructPermutatMat (F one, int dim)
	throws IllegalArgumentException {
		if(one.isZero()) throw new IllegalArgumentException ("\nZero element cannot generate a non-tirivial space!!!");
		if(dim<maxArg) throw new IllegalArgumentException ("\nDimension must be greater or equal to maximal argument");
		int length = length();		
		if(length==0) return AbstractMatrix.identity(one, dim);
		AbstractMatrix<F> perm = new AbstractMatrix<F> (dim);
		Integer first = null, last = null;
		Iterator<Cycle> cycleIt = cycleMap.iterator();
		HashSet<Integer> indices = new HashSet<Integer> ();
		while (cycleIt.hasNext()) {
			Cycle cycle = cycleIt.next();
			Iterator<Integer> intIt = cycle.iterator();
			while(intIt.hasNext()){
				Integer inCycle = intIt.next();
				if(first==null) first = inCycle;
				if(last!=null) perm.setEntry(inCycle, last, one);
				//else if(!intIt.hasNext()) perm.setEntry(last,inCycle, one);
				last = inCycle;
				indices.add(inCycle);
			}
			if(last!=null&&first!=null) perm.setEntry(first, last, one);
			if(cycleIt.hasNext()){
				first = null;
				last  = null;
			}
		}
		//if(!cycleIt.hasNext()&&last!=null&&first!=null) perm.setEntry(last, first, one);
		if(dim!=indices.size()) {
			for (int i = 0; i < dim;i++) if(!indices.contains(i)&&perm.getValue(i, i)==null) perm.setEntry(i, i, one);
		}
		return perm;
	}
	/**
	 * Returns a square permutation matrix object representing
	 * this permutation
	 * @param one some non-zero element
	 * @return the permutation matrix
	 * @throws IllegalArgumentException if <code>one.isZero()</code> returns
	 * true 
	 */
	public <F extends AbstractField<F>> AbstractMatrix<F> constructPermutatMat(F one){
		setMaxArg();
		return constructPermutatMat(one,maxArg);
	}
	
	public boolean equals(SymmetricGroup<X> another) {
		if(this==another) return true;
		return cycleMap.equals(another.cycleMap)?true:false;
	}
	
	public void f() {
		if(val==null) val = new Tuple <X> ();
		if(arg==null) return;
		for (Cycle cycle : cycleMap) {
			Iterator<Entry<Integer,Integer>> it = cycle.cycleMap.entrySet().iterator();
			while(it.hasNext()){
				Entry<Integer,Integer> cycleEntry = it.next();
				X entry;
				if((entry = arg.getValue(cycleEntry.getKey()))!=null) val.setEntry(cycleEntry.getValue(), entry);
			}
		}
	}
	public void f(Tuple<X> arg){this.arg = arg; f();}
	
	public Tuple<X> getArgument (){return arg;}
	public SymmetricGroup<X> getConjugate(SymmetricGroup<X> another){
		//TODO implement me
		if(length()!=another.length()) return null;
		Iterator<Cycle> it1 = cycleMap.iterator(), it2 = another.cycleMap.iterator();
		while (it1.hasNext()||it2.hasNext()){
			Cycle cycle1 = null, cycle2 = null;
			if(it1.hasNext()) cycle1 = it1.next();
			if(cycle1!=null) {
				boolean found = false;
				while (it2.hasNext()) {
					cycle2 = it2.next();
					if(cycle1.length==cycle2.length){
						found = true;
						break;
					}
				}
				if(found) break;
				else return null;
			}
		}
		return null;
	}
	/**
	 * Returns a <code>Cycle</code> object containing the argument
	 * <tt>index</tt> or null if this permutation contains no such cycle
	 * @param index some index
	 * @return the containing cycle
	 */
	public Cycle getCycle (int index) {
		for (Cycle cycle:cycleMap) if(cycle.cycleMap.containsKey(index)) return cycle;
		return null;		
	}
	/**
	 * Returns an ordered set of all disjoint cycles
	 * of this permutation
	 * @return a cycle set
	 */
	public TreeSet<Cycle> getCycleSet(){
		TreeSet<Cycle> cp = new TreeSet<Cycle> ();
		for (Cycle cycle : cycleMap) cp.add(new Cycle(cycle));
		return cp;
	}
	/**
	 * Returns the highest integer entry in this permutation
	 * @return
	 */
	public int getMaxArg(){return maxArg;}
	public Tuple<X> getValue (){return val;}
	/**
	 * Returns the inverse permutation of this such that
	 * <tt>this.inverse().multiply(this)</tt> equals the identity
	 * @return the inverse
	 */
	public SymmetricGroup<X> inverse(){
		SymmetricGroup<X> inv = new SymmetricGroup<X> ();
		for (Cycle cycle:cycleMap) inv.cycleMap.add(cycle.inverse());
		return inv;
	}
	public boolean isKernel(){
		//@SuppressWarnings("unchecked")
		SymmetricGroup<Object> cp = new SymmetricGroup<Object>();
		for (Cycle cycle:cycleMap) cp.cycleMap.add(cycle);
		SIGN.f(cp);
		return SIGN.getValue().equals(TwoCycle.ZERO)?true:false;
	}
	/**
	 * Returns the length of this permutation - the sum of the
	 * length of all disjoint cycles in this permutation 
	 * @return the length
	 */
	public int length(){
		int length = 0;
		for (Cycle cycle:cycleMap) {
			if(cycle.isClosed())
				length += cycle.length-1;
		}
		return length;
	}
	/**
	 * Returns the product permutation (composition <tt>this * another</tt>)
	 */
	public SymmetricGroup<X> multiply (SymmetricGroup<X> another){
		//if either of the two permutation is identity nothing to compute
		if(cycleMap.size()==0||another.cycleMap.size()==0) return cycleMap.size()==0?new SymmetricGroup<X> (another):new SymmetricGroup<X> (this);
		
		//the product permutation
		SymmetricGroup<X> prod = new SymmetricGroup <X> ();
		
		//iterators over each cycle entry from this and another
		//left: this - right: another
		Iterator<Cycle> itLeft = cycleMap.iterator(), itRight = another.cycleMap.iterator();
		
		//cycle objects from this and another plus a new cycle for the
		//product permutation
		//left: this - right: another
		Cycle c1Left = null, c2Left = null, c1Right = null, c2Right = null, cycle = new Cycle();
		
		//sanity check: the cycle should never be empty
		if(itLeft.hasNext()) c1Left = itLeft.next();
		
		//sanity check: the cycle should never be empty
		if(itRight.hasNext()) c1Right = itRight.next();
		
		//the integer key/value objects for the new cycle object
		//and the first integer: the first key to be added to the cycle
		Integer key = null, val = null, first = null;
		
		//iterators over the first cycles of this and another (left, right)
		Iterator<Integer> cycleItL = c1Left.iterator(), cycleItR = c1Right.iterator();
		
		//sanity check: right cycle iterator should never be empty here
		if(cycleItR.hasNext()) key = cycleItR.next();
		
		//left/right switch (flag)
		boolean leftFlag = false;
		
		//iterate over all cycles
		while (true){
			//set the first key 
			if(first==null) first = key;
			
			//last key came from this (left)
			if(leftFlag){
				
				//find a matching cycle in another
				c2Right = another.getCycle(key);
				
				//is there a matching cycle?
				if(c2Right!=null) {
					
					//get the intermediate value
					Integer inter = c2Right.getValue(key);
					
					//does the intermediate value have a matching cycle in
					//this permutation?
					if((c2Left = getCycle(inter))!=null) {val = c2Left.getValue(inter); leftFlag = true;}
					
					//if no such cycle found
					else {val = inter; leftFlag = false;}
					
				}
				
				//no matching cycle then use its value
				else val = c2Left.getValue(key);
			}
			
			//last key came from another (right)
			else {
				
				//get the intermediate value
				Integer keys = c1Right.getValue(key);
				
				//get its corresponding cycle from this (left)
				c2Left = getCycle(keys);
				
				//if there is some cycle
				if(c2Left!=null) {
					val = c2Left.getValue(keys);
					leftFlag = true;
				}
				
				//no such cycle found
				else {val = keys;leftFlag = false;}
			}
			//only if first!=val and key!=val add the key value pair
			//to the current cycle object
			if(!first.equals(val)&&!key.equals(val)) {cycle.cycleMap.put(key,val);key = val;}
			
			//either first==val or key==val then:
			else {
				
				//if first==val the cycle is completed
				//then add the cycle to the product and
				//construct a new cycle
				if(!key.equals(val)) {
					cycle.cycleMap.put(key, val);
					prod.cycleMap.add(cycle);
					cycle = new Cycle();
				}
				
				//delete the first key
				first = null;
				
				//get the next key - first test if another has some unused
				//key in the current cycle, if not get the next cycle from right (another)
				boolean itRHasNext = itRight.hasNext(), cycleRHasNext = cycleItR.hasNext();
				boolean breakFlagR = false, breakFlagL = false;
				if(itRHasNext||cycleRHasNext){
					
					//iterator over all cycles from right
					while(true){
						
						//iterate over each of its cycle elements
						while(cycleItR.hasNext()) {
							
							//get the entry of the cycle
							key = cycleItR.next();
							
							//does the product contain such a
							//cycle already?
							if(prod.getCycle(key)==null){
								
								//if not use the current key and continue
								breakFlagR = true;
								break;
							}
						}
						
						//break the outer loop
						if(breakFlagR) break;
						
						//otherwise get a new cycle and repeat
						//until either no more cycles or a new key is found 
						if(itRight.hasNext()) {c1Right = itRight.next(); c2Right = c1Right; cycleItR = c1Right.iterator();}
						else break;
					}
					
					//new key was found in another
					leftFlag = false;
					
				}
				//in case no new key found in another (right) repeat the same
				//for the left
				if(!breakFlagR&&(itLeft.hasNext()||cycleItL.hasNext())){
					while(true){
						//iterator over all left cycles
						while(cycleItL.hasNext()){
							
							//the cycle iteration
							key = cycleItL.next();
							
							//if the is some unused key, get it
							if(prod.getCycle(key)==null) {
								breakFlagL = true;
								break;
							}
						}
						
						//break the outer loop
						if(breakFlagL) break;
						
						//no key found, then get a new cycle and repeat
						//until no more cycles or a new key is found
						if(itLeft.hasNext()) {c1Left = itLeft.next(); cycleItL = c1Left.iterator();}
						else break;
					}
					
					//new key found in this
					leftFlag = true;
				}
				
				//reset the left and right cycles
				//to the currently selected ones
				c2Right = c1Right;
				c2Left = c1Left;
				
				//if either no new key from left or right we are done
				//because no more cycles left to check - 
				//no need to iterate any more
				if(!breakFlagR&&!breakFlagL) break;

			}
		}
		
		//compute the maximal argument
		prod.setMaxArg();
		
		//return the product
		return prod;
	}
	/**
	 * Returns the order of this permutation
	 * @return the order
	 */
	public int ord(){
		if(cycleMap.size()==0) return 1;
		int ord = 1;
		TreeMap<Integer,Integer> orderMap = new TreeMap<Integer,Integer> ();
		for (Cycle cycle:cycleMap){
			int length = cycle.length;
			if(orderMap.get(length)==null) {
				boolean inMap = false;
				Iterator<Entry<Integer,Integer>> it = orderMap.entrySet().iterator();
				while(it.hasNext()){
					Entry<Integer,Integer> entry = it.next();
					if(inMap&&length%entry.getKey()==0) it.remove();
					if(length%entry.getKey()==0){
						if(length>entry.getValue()){
							inMap = true;
							entry.setValue(length);
						}
					}
				}
				if(!inMap) {
					orderMap.put(length, length);
				}
			}
		}
		for (Integer values:orderMap.values()) ord *= values;
		return ord;
	}
	public String toString (){
		return cycleMap.toString();
	}
	/*--------------------privates------------------------*/
	/**
	 * Auxiliary method: decomposes the array entries to a set of disjoint
	 * cycles
	 * @param cycleArray
	 */
	private void decomposeCycleArray (int[] cycleArray){
		int length  = cycleArray.length;
		int firstIn = -1, lastIn = -1;
		Cycle cycle = new Cycle (), testCycl = null;
		for (int i = 0; i < length; i++){
			if(i<length-1&&cycleArray[i]==cycleArray[i+1]) continue;
			boolean isKey = cycle.cycleMap.containsKey(cycleArray[i]), isVal = cycle.cycleMap.containsValue(cycleArray[i]);
			if((testCycl = getCycle(cycleArray[i]))==null&&!isKey&&!isVal){
				if(firstIn==-1&&lastIn==-1) {firstIn = cycleArray[i];lastIn = cycleArray[i];}
				else {cycle.cycleMap.put(lastIn, cycleArray[i]); lastIn = cycleArray[i];}
				
			}
			else{
				if(testCycl==null&&isKey&&!isVal){
					cycle.cycleMap.put(lastIn,cycleArray[i]);
				}
				else {
					if(testCycl==null&&!isKey&&isVal) cycle.cycleMap.put(cycleArray[i],firstIn);
					else {
						cycle.cycleMap.put(lastIn, firstIn);
					}
				}
				if(cycle.isClosed()) {
					//if(cycle.first==null) cycle.first = firstIn;
					cycleMap.add(cycle);
				}
				firstIn = -1; lastIn = -1;
				cycle = new Cycle ();
			}
		}
		
		if(!cycle.isIdentity()) {
			if(!cycle.isClosed()) cycle.cycleMap.put(lastIn, firstIn);
			cycleMap.add(cycle);
		}
		
		setMaxArg();
	}
	/**
	 * Auxiliary method: decomposes the array of objects
	 * to a set of disjoint cycles
	 * @param cycleArray
	 */
	private void decomposeCycleArray(X[] cycleArray){
		int length = cycleArray.length, index = 0;
		int[] cyclAr = new int[length];
		X entry = null;
		for (int i = 0; i < length; i++){
			if(i==0) {entry = cycleArray[i]; index = i;continue;}
			if(cycleArray[i]!=null){
				if(entry!=null&&entry.equals(cycleArray[i])) cyclAr[i] = index;
				else{
					//index = i;
					cyclAr[i] = i;
					//entry = cycleArray[i];
				}
			}
		}
		decomposeCycleArray(cyclAr);
	}
	/**
	 * Setter: sets the the greatest element
	 * in all cycles 
	 */
	private void setMaxArg(){
		for (Cycle cycle1:cycleMap) {
			for (Integer inCycle:cycle1) if(inCycle>=maxArg) maxArg = inCycle+1;
		}
	}
	/*-------------------------nested classes-----------------------------*/
	/**
	 * The cycle class
	 * @author adin
	 *
	 */
	public final static class Cycle implements Iterable<Integer>, Comparable<Cycle>{
		/**the length of the cycle - its cardinality*/
		int length;
		/**the maximal value in the cycle*/
		int maxValue;
		/**the first key in the cycle*/
		Integer first;
		/**the cycle map*/
		private TreeMap<Integer,Integer> cycleMap;
		/**
		 * Constructs an empty cycle - the identity
		 */
		Cycle (){
			cycleMap = new TreeMap<Integer,Integer> ();
		}
		/**
		 * Copies the argument <tt>cycle</tt> if
		 * <code>cycle.isClosed()</code> returns true
		 * @param cycle another cycle
		 */
		Cycle (Cycle cycle){
			this();
			if(cycle.isClosed()){
				cycleMap.putAll(cycle.cycleMap);
				isClosed();
			}
		}
		public int compareTo (Cycle another){
			isClosed();
			another.isClosed();
			if(length!=another.length) return length<another.length?-1:length>another.length?1:0;
			Iterator<Integer> thisIt = iterator(), anothIt = another.iterator();
			while(true) {
				Integer thisNext = null, anothNext = null;
				if(thisIt.hasNext()) thisNext = thisIt.next();
				if(anothIt.hasNext()) anothNext = anothIt.next();
				if(thisNext==null||anothNext==null) break;
				if(thisNext.equals(anothNext)) continue;
				if(thisNext<anothNext) return -1;
				return 1;
			}
			return 0;
		}
		public boolean equals (Object o){
			if(this==o) return true;
			if(!(o instanceof Cycle)) return false;
			Cycle cp = (Cycle) o;
			if(length!=cp.length) return false;
			Integer first = getFirst();
			Integer val1 = getValue(first), val2 = cp.getValue(first);
			if(val2==null) return false;
			while (!val1.equals(first)) {
				if(val1.equals(val2)) {val1 = getValue(val1);val2 = cp.getValue(val2);continue;}
				return false;
			}
			return true;
		}
		public Integer getFirst (){return first;}
		/**
		 * Returns the key associated to the <tt>value</tt> or null
		 * if no such key-value pair exists
		 * @param value
		 * @return
		 */
		public Integer getKey (int value){
			for (Map.Entry<Integer, Integer> entry:cycleMap.entrySet()) {
				if(entry.getValue().equals(value)) return entry.getKey();
			}
			return null;
		}
		/**
		 * Returns the value associated to the <tt>key</tt> or null
		 * if no such key-value pair exists
		 * @param key
		 * @return
		 */
		public Integer getValue (int key){
			Integer val = null;
			return (val = cycleMap.get(key))==null?null:val;
			
		}
		public int hashCode (){
			int hash = 0;
			Iterator<Integer> it = iterator();
			Integer key = null, val = null;
			while (it.hasNext()) {
				val = it.next();
				if(key==null) hash += val;
				else hash += key*val;
				key = val;
			}
			return hash;
		}
		/**
		 * Returns the inverse cycle of this
		 * @return the inverse
		 */
		public Cycle inverse(){
			Cycle inv = new Cycle ();
			for (Entry<Integer,Integer> entry:cycleMap.entrySet()) inv.cycleMap.put(entry.getValue(), entry.getKey());
			inv.isClosed();
			return inv;
		}
		/**
		 * Returns true if and only if all key values are present in the value set
		 * (and visa versa)
		 * @return
		 */
		public boolean isClosed (){
			Set<Integer> keys = cycleMap.keySet();
			length = keys.size();
			if(length==0) return false;
			if(first==null){first = cycleMap.firstKey();}
			Collection<Integer> vals = cycleMap.values();			
			return keys.containsAll(vals)&&vals.containsAll(keys)?true:false;}
		public boolean isDisjoint (Cycle another){return cycleMap.keySet().contains(another.cycleMap.keySet())||another.cycleMap.keySet().contains(cycleMap.keySet())?false:true;
		}
		/**
		 * Returns true if this cycle is of length zero
		 * @return
		 */
		public boolean isIdentity (){return cycleMap.size()==0?true:false;}
		/**
		 * Returns an iterator of this cycle object - note the sequence of
		 * elements returned by successive calls to the <code>next()</code> method follows the convention:<br />
		 * <tt>(x,getVal(x),getVal(getValue(x)),...,getValue(...(getValue(x)...)))</tt> for some element <tt>x</tt> in
		 * this cycle. <p>Remove operation is not supported - leaving the cycle unaltered
		 */
		public Iterator<Integer> iterator() {return new CycleIterator ();}
		public String toString (){
			StringBuilder sb = new StringBuilder ("(");
			String comma = ",";
			Iterator<Integer> it = iterator();
			while(it.hasNext()) {
				sb.append(it.next());
				if(it.hasNext()) sb.append(comma); 
			}
			sb.append(")");
			return sb.toString();
		}
		/**
		 * Cycle iterator class - the iterator has the following properties:
		 * <ol>
		 * <li>if this cycle is not empty: {@link Iterator#hasNext()} will return true prior to the first
		 * step (calling {@link Iterator#next()})</li>
		 * <li>the first element returned is the lowest value in the entry list - the so called <b>first key</b></li>
		 * <li>each following value is the image of the previous value</li>
		 * <li>the iteration is exhausted (<code>hasNext()</code> returns false), when the next value equals the first key</li>
		 * </ol>
		 * @author adin
		 *
		 */
		private class CycleIterator implements Iterator<Integer> {
			/**the current value*/
			private Integer current;
			/**the next value or null*/
			private Integer    next;
			/**flag indicating, whether the <code>next()</code> method
			 * has been called*/
			private boolean firstEn       = true;
			/**
			 * Constructs a cycle iterator starting at
			 * the first key
			 */
			private CycleIterator (){
				isClosed();
				if(first!=null){
					current = new Integer(first);
					next = getValue(first);
				}
			}
			/**
			 * Returns true until the next value equals the first
			 * key
			 */
			public boolean hasNext (){
				if(first==null) return false;
				if(firstEn) {return true;}
				return current.equals(first)?false:true;
			}
			/**
			 * Returns the next value
			 */
			public Integer next (){
				if(firstEn) firstEn = false;
				Integer cp = current;
				current = next;
				next = cycleMap.get(current);
				return cp;
			}
			/**
			 * Unsupported operation - does not change this cycle
			 */
			public void remove(){
				return;
			}
			
		}
	}
	/**
	 * The sign group homomorphism: maps each permutation to an element of the cyclic group
	 * of order two (here {@link TwoCycle}):
	 * <br /><code>SymmetricGroup&ltObject&gt  perm = new SymmetricGroup(....</code><br />
	 * <code>SIGN.f(perm).equals(TwoCycle.ZERO)</code> returns 
	 * <ol><li>true, if the number of generating transposition is even</li>
	 * <li>false, if the number of generating transposition is odd</li></ol>
	 * @author adin
	 *
	 * @param <X>
	 */
	public final static class Sign<X> implements GroupHomo<Sign<X>,SymmetricGroup<X>,TwoCycle> {
		/**the argument permutation*/
		private SymmetricGroup<X> arg;
		/**the sign value*/
		private TwoCycle val;
		/**
		 * The only constructor is private - no
		 * instantiation outside the outer class permitted
		 */
		private Sign (){}
		
		public synchronized void setArgument(SymmetricGroup<X> arg) {this.arg = arg;}

		
		public synchronized void f() {
			if(arg==null) return;
			if(arg.length()%2==0) val = TwoCycle.ZERO;
			else val = TwoCycle.ONE;
		}

		
		public void f(SymmetricGroup<X> arg) {
			setArgument(arg);
			f();
		}

		
		public SymmetricGroup<X> getArgument() {return arg;}

		
		public TwoCycle getValue() {return val;}
		
	}
	public static void main (String[] args){
		Object o1 = new Object(), o2 = new Object(), o3 = new Object();
		Object[] o = new Object[]{o1,o2,o1,new Object(),new Object(), new Object(),o1,o3,new Object(), new Object(), new Object(),new Object(),new Object(), new Object(), new Object(), new Object()};
		Tuple<Object> t = new Tuple<Object> ();
		t.setEntry(0, o1);
		t.setEntry(1, o2);
		t.setEntry(2, o3);
		SymmetricGroup<Object> cycle = new SymmetricGroup<Object> (o);
		System.out.println(cycle);
		AbstractMatrix<Rational> mat = cycle.constructPermutatMat(Rational.ONE), mat2 = new AbstractMatrix<Rational> (mat);
		System.out.println(mat);
		SymmetricGroup<Object> cyc = new SymmetricGroup<Object> (cycle),id = new SymmetricGroup<Object> ();
		//SymmetricGroup<Object> trp = new SymmetricGroup<Object> (new int[]{2,5});
		int i = 1;
		long start1 = 0, start2 = 0, end1 = 0, end2 = 0;
		double meanCompTimeCycle = 0, meanCompTimeMatrx = 0;
		while (!cyc.equals(id)) {
			StringBuilder sb = new StringBuilder(String.format("pi^%2$d =\t\t\t%1$s",cyc,i));
			sb.append("\n");
			if(i!=1){
				double compCycle = ((double) end1-start1)*1e-9;
				double compMatrx = ((double) end2-start2)*1e-9;
				sb.append(String.format("exe time (cycle operation):\t%1$g sec",compCycle));
				sb.append("\n");
				sb.append(String.format("exe time (matrix operation):\t%1$g sec",compMatrx));
				sb.append("\n");
				meanCompTimeCycle += compCycle;
				meanCompTimeMatrx += compMatrx;
			}
			//long start1 = System.nanoTime();
			//SymmetricGroup<Object> conj = trp.multiply(cyc.multiply(trp));
			//long end1   = System.nanoTime();
			//System.out.println(String.format("%1$s pi %1$s =\t%2$s",trp.toString(),conj.toString()));
			
			//sb.append(String.format("exe time: %1$g",((double) end1-start1)*1e-9));
			//sb.append("\n");
			//System.out.println();
			//System.out.println(conj.multiply(cyc).inverse().multiply(conj.inverse()));
			//AbstractMatrix<Rational> co   = cyc.constructPermutatMat(Rational.ONE,cycle.maxArg);
			//long start2 = System.nanoTime();
			AbstractMatrix<Rational> testMat = cyc.constructPermutatMat(Rational.ONE, cycle.maxArg);
			if(!mat.equals(testMat))
				System.err.println(String.format("Matrix mismatch - wrong matrix\n%1$s",mat.toString()));
			sb.append(String.format("permutation matrix:\n%1$s",testMat));
			//System.out.println();
			if(cyc.isKernel()) {System.out.println(sb.toString());System.out.flush();}
			else {System.err.println(sb.toString());System.err.flush();}
			
			//System.out.println(String.format("mat(pi^%3$d) = \n%1$s\n%2$g",prod.toString(),((double) end2 - start2)*1e-9,i));
			if(i==8)
				System.gc();
			start1 = System.nanoTime();
			cyc = cyc.multiply(cycle);
			end1 = System.nanoTime();
			start2 = System.nanoTime();
			mat = mat.multiply(mat2);
			end2 = System.nanoTime();
			i++;
			System.gc();
		}
		System.out.println(String.format("order computed1: %1$d \torder computed2: %2$d\nmean exe time (cycle):\t%3$g sec\nmean exe time (matrx):\t%4$g sec",cycle.ord(),i,meanCompTimeCycle/i,meanCompTimeMatrx/i));
	}
	
	
}