package group;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map.Entry;

import util.Function;
import util.Tuple;
/**
 * Second implementation of the symmetric group - the set of all bijections
 * of a finite set. This class is a subtype of {@link AbstractNAG} as well as
 * {@link Function}. 
 * @author adin
 *
 * @param <X> the type of the underlying set
 */
public class SymmetricGroup2<X> extends AbstractNAG<SymmetricGroup2<X>> implements
		Function<Tuple<X>,Tuple<X>> {
	private int              maxArg;
	private Tuple<X>            arg;
	private Tuple<X>            val;	
	private HashSet<Cycle> cycleSet;
	/**
	 * Constructs the identity element
	 */
	public SymmetricGroup2 (){
		super();
		cycleSet = new HashSet<Cycle> ();
	}
	/**
	 * Constructs an object with disjoint cycles
	 * specified by the argument array <tt>cycleArray</tt>.
	 * The following convention holds:<br />
	 * <ol>
	 * <li>if <tt>cycleArray[i]!=cycleArray[i+k]</tt> returns true for some indices <tt>i, k &gt 0</tt>
	 * this permutation contains a cycle of the form <tt>(...,cycleArray[i],cycleArray[i+k],...)</tt></li>
	 * <li>consecutive repetitions are omitted - such that <tt>{0,0,0,1,2}</tt> equals the cycle <tt>(0,1,2)</tt></li>
	 * <li><b>Note</b>, however, that interspersed repetitions close the previous cycle, to specify:
	 *  <tt>(0,0,1,0,2)</tt> equals the cycle <tt>(0,1)</tt>
	 * </li>
	 * </ol>
	 * @param cycleArray
	 */
	public SymmetricGroup2 (int[] cycleArray){
		this();
		decomposeCycleArray(cycleArray);
	}
	/**
	 * Constructs an object of this class specified by the argument array <tt>cycleArray</tt>
	 * @param cycleArray
	 */
	public SymmetricGroup2 (X[] cycleArray){
		this();
		decomposeCycleArray(cycleArray);
	}
	public SymmetricGroup2 (Cycle cycle){
		this();
		cycleSet.add(cycle);
		setMaxArg();
	}
	public SymmetricGroup2 (SymmetricGroup2<X> another){
		this();
		for (Cycle cycle:another.cycleSet) cycleSet.add(cycle);
		setMaxArg();
	}
	public boolean equals(SymmetricGroup2<X> another) {
		if(this==another) return true;
		if(cycleSet.size()!=another.cycleSet.size()) return false;
		if(maxArg!=another.maxArg) return false;
		return cycleSet.equals(another.cycleSet)?true:false;
	}
	
	



	
	public void f() {
		if(arg==null) return;
		if(val==null) val = new Tuple<X> ();
		for (Cycle cycle : cycleSet){
			for (Entry<Integer,Integer> cycleEntry:cycle.cycle.entrySet()){
				Integer argIndex = cycleEntry.getKey(), valIndex = cycleEntry.getValue();
				X entry = null;
				if((entry = arg.getValue(argIndex))!=null) val.setEntry(valIndex, entry);
			}
		}
		for (Entry<Integer,X> entry : arg){
			if(getCycle(entry.getKey())==null) val.setEntry(entry.getKey(), entry.getValue());
		}
	}


	
	public void f(Tuple<X> arg) {
		if(arg!=null){
			this.arg = arg;
			f();
		}
	}


	
	public Tuple<X> getArgument() {return arg==null?null:arg;}
	/**
	 * Returns a cycle element <tt>c</tt> such that 
	 * @param index
	 * @return
	 */
	public Cycle getCycle(int index){
		for (Cycle cycle:cycleSet) {if(cycle.cycle.containsKey(index)) return cycle;}
		return null;
	}

	
	public Tuple<X> getValue() {
		if(val!=null) return val;
		if(arg!=null){
			f();
			return val;
		}
		return null;
	}
	

	
	public SymmetricGroup2<X> multiply(SymmetricGroup2<X> another) {
		SymmetricGroup2<X> prod = new SymmetricGroup2<X> ();
		if(cycleSet.size()==0&&another.cycleSet.size()==0) return prod;
		if(cycleSet.size()==0) return new SymmetricGroup2<X> (another);
		if(another.cycleSet.size()==0) return new SymmetricGroup2<X>(this);
		Iterator<Cycle> rightCycles = another.cycleSet.iterator(), leftCycles = cycleSet.iterator();
		Cycle cycleR1 = null, cycleR2 = null, cycleL1 = null, cycleL2 = null, newCycle = new Cycle();
		if(rightCycles.hasNext()) cycleR1 = rightCycles.next();
		if(leftCycles.hasNext())  cycleL1 = leftCycles.next();
		Integer key = null, val = null, first = null;
		Iterator<Integer> cycleRight = cycleR1.iterator(), cycleLeft = cycleL1.iterator();
		if(cycleRight.hasNext()) {key = cycleRight.next(); first = key;}
		while(key!=null) {
			Integer inter = null;
			if((inter = cycleR1.cycle.get(key))!=null) {
				cycleL2 = getCycle(inter);
				if(cycleL2==null) val = inter;
				else val = cycleL2.cycle.get(inter);
			}
			else {
				cycleR2 = another.getCycle(key);
				if(cycleR2!=null){
					if((inter = cycleR2.cycle.get(key))!=null) {
						cycleL2 = getCycle(inter);
						if(cycleL2==null) val = inter;
						else {val = cycleL2.cycle.get(inter);}
					}
				}
				else {
					cycleL2 = getCycle(key);
					if(cycleL2!=null) val = cycleL2.cycle.get(key);
				}
			}
			if(!first.equals(val)&&!key.equals(val)) {newCycle.add(key, val);key = val;}
			else {
				boolean left = false, right = false;
				if(!key.equals(val)) {
					newCycle.add(key,val);
					if(newCycle.isClosed()) prod.cycleSet.add(newCycle);
					newCycle = new Cycle();
				}
				while(true) {
					while(cycleRight.hasNext()) {
						Integer next = cycleRight.next();
						if(prod.getCycle(next)==null) {
							key = next;
							first = key;
							right = true;
							break;
						}
					}
					if(right) break;
					if(rightCycles.hasNext()){
						cycleR1 = rightCycles.next();
						cycleRight = cycleR1.iterator();
					}
					else break;
				}
				if(!right){
					while(true){
						while(cycleLeft.hasNext()){
							Integer next = cycleLeft.next();
							if(prod.getCycle(next)==null&&another.getCycle(next)==null){
								key = next;
								first = key;
								left = true;
							}
						}
						if(left) break;
						if(leftCycles.hasNext()){
							cycleL1 = leftCycles.next();
							cycleLeft = cycleL1.iterator();
						}
						else break;
					}
				}
				if(!right&&!left) break;
			}
		}
		prod.setMaxArg();
		return prod;
	}
	/**
	 * Returns the inverse permutation <tt>this^-1</tt>, such that
	 * <code>multiply(inverse()).equals(new SymmetricGroup2())</code>
	 * returns true (identity)
	 * @return
	 */
	public SymmetricGroup2<X> inverse (){
		SymmetricGroup2<X> inv = new SymmetricGroup2<X> ();
		for (Cycle cycle:cycleSet) inv.cycleSet.add(cycle.inverse());
		return inv;
	}
	/**
	 * Sets the argument of the this object
	 * @param arg the argument
	 */
	public void setArgument(Tuple<X> arg){
		if(arg!=null) this.arg = arg;
	}
	public String toString(){return cycleSet.toString();}
	/*------------------privates----------------------------*/
	/**
	 * Auxiliary method: decomposes the array entries to a set of disjoint
	 * cycles
	 * @param cycleArray an array of <tt>int</tt>s
	 */
	private void decomposeCycleArray (int[] cycleArray){
		int length  = cycleArray.length;
		int firstIn = -1, lastIn = -1;
		Cycle cycle = new Cycle (), testCycl = null;
		for (int i = 0; i < length; i++){
			if(i<length-1&&cycleArray[i]==cycleArray[i+1]) continue;
			boolean isKey = cycle.cycle.containsKey(cycleArray[i]), isVal = cycle.cycle.containsValue(cycleArray[i]);
			if((testCycl = getCycle(cycleArray[i]))==null&&!isKey&&!isVal){
				if(firstIn==-1&&lastIn==-1) {firstIn = cycleArray[i];lastIn = cycleArray[i];}
				else {cycle.add(lastIn, cycleArray[i]); lastIn = cycleArray[i];}
				
			}
			else{
				if(testCycl==null&&isKey&&!isVal){
					cycle.add(lastIn,cycleArray[i]);
				}
				else {
					if(testCycl==null&&!isKey&&isVal) cycle.add(cycleArray[i],firstIn);
					else {
						cycle.add(lastIn, firstIn);
					}
				}
				if(cycle.isClosed()) {
					//if(cycle.first==null) cycle.first = firstIn;
					cycleSet.add(cycle);
				}
				firstIn = -1; lastIn = -1;
				cycle = new Cycle ();
			}
		}
		
		if(!cycle.isIdentity()) {
			if(!cycle.isClosed()) cycle.add(lastIn, firstIn);
			cycleSet.add(cycle);
		}
		
		setMaxArg();
	}
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
	private void setMaxArg (){
		for (Cycle cycle:cycleSet){
			for(Integer index:cycle){
				if(maxArg<=index+1) maxArg = index+1; 
			}
		}
	}
	/*------------------statics-----------------------------*/
	public static class Cycle implements Iterable<Integer>{
		private HashMap<Integer,Integer>    cycle;
		private HashMap<Integer,Integer> invCycle;
		private int hash;
		private Integer first;
		private Cycle (){
			cycle    = new HashMap<Integer,Integer> ();
			invCycle = new HashMap<Integer,Integer> ();
		}
		Cycle (Cycle cycle){
			this();
			for (Entry<Integer, Integer> entry:cycle.cycle.entrySet()) add(entry.getKey(),entry.getValue());
		}
		/**
		 * Adds an entry to this cycle object and returns true
		 * iff the addition was successful
		 * @param key the key
		 * @param value the value
		 * @return true iff addition successful
		 */
		private boolean add(int key, int value){
			boolean keyInCycle = cycle.containsKey(key), valInCycle = cycle.containsValue(value);
			boolean keyInInv   = invCycle.containsKey(value), valInInv = invCycle.containsValue(key);
			if(!keyInCycle&&!valInCycle&&!keyInInv&&!valInInv){
				if(first==null) first = key;
				else if(first.compareTo(key)>0) first = key;
				cycle.put(key, value);
				invCycle.put(value, key);
				if(key<value)hash += key*value+(key+1)*value;
				else hash += key*value-(key+1)*value;
				return true;
			}
			return false;
		}
		public HashSet<Cycle> compose (Cycle another){
			HashSet<Cycle> cycleSet = new HashSet<Cycle>();
			if(isDisjoint(another)) {
				cycleSet.add(this);
				cycleSet.add(another);
				
			}
			else  {
				HashSet<Integer> addSet = new HashSet<Integer>();
				Iterator<Integer> rightIt = another.iterator(), leftIt = iterator();
				Integer first = null, key = null, val = null;
				boolean left = false;
				Cycle newCycle = new Cycle();
				if(rightIt.hasNext()) {first = rightIt.next(); key = first;}
				while(key!=null) {
					if(left) {
						Integer inter = another.cycle.get(key);
						if(inter!=null) {
							if((val = cycle.get(inter))==null){val = inter;left = false;}
							else left = true;
						}
						else{
							val = getValue(key);
							left = true;
						}
					}
					else{
						Integer inter = another.cycle.get(key);
						if(inter!=null) {
							if((val = cycle.get(inter))==null) {val = inter;left = false;}
							else left = true;
						}
					}
					addSet.add(key);
					if(!first.equals(val)&&!key.equals(val)) {newCycle.add(key, val);key = val;}
					else {
						if(!key.equals(val)) {
							//addSet.add(key);
							newCycle.add(key, first);
							cycleSet.add(newCycle);
							newCycle = new Cycle();
						}
						boolean leftBreak = false, rightBreak = false;
						while(rightIt.hasNext()){
							Integer next = rightIt.next();
							if(!addSet.contains(next)) {first = next; key = next; rightBreak = true;left = false;break;}
						}
						if(!rightBreak){
							while (leftIt.hasNext()){
								Integer next = leftIt.next();
								if(!addSet.contains(next)){first = next; key = next; leftBreak = true;left = true;break;}
							}
						}
						if(!rightBreak&&!leftBreak) break;
					}
				}
			}
			return cycleSet;
		}
		public boolean equals(Object o){
			if(this==o) return true;
			if(!(o instanceof Cycle)) return false;
			Cycle cp = (Cycle) o;
			if(hash!=cp.hash) return false;
			if(cycle.size()!=cp.cycle.size()) return false;
			if(!first.equals(cp.first)) return false;
			Iterator<Integer> it1 = iterator(), it2 = cp.iterator();
			while(it1.hasNext()&&it2.hasNext()){
				Integer val1 = it1.next(), val2 = it2.next();
				if(!val1.equals(val2)) return false;
			}
			if(it1.hasNext()||it2.hasNext()) return false;
			return true;
		}
		public Integer getKey (int value){
			Integer key = invCycle.get(value);
			return key==null?null:key;
		}
		public Integer getValue(int key){
			Integer val = cycle.get(key);
			return val==null?null:val;
		}
		public int hashCode(){return hash;}
		public Cycle inverse (){
			Cycle inv = new Cycle ();
			for (Entry<Integer,Integer> entry:cycle.entrySet()) inv.add(entry.getValue(), entry.getKey());
			return inv;
		}
		public boolean isClosed(){
			HashSet<Integer> keySet = new HashSet<Integer>(cycle.keySet()), valSet = new HashSet<Integer>(cycle.values());
			if(!keySet.equals(valSet)) return false;
			Iterator<Integer> it = iterator();
			while(it.hasNext()) {
				Integer val = it.next();
				if(val==null) return false;
			}
			return true;
		}
		public boolean isDisjoint(Cycle another){
			Iterator<Integer> it = iterator();
			int count = 0;
			while(count==0){
			while(it.hasNext()){
				Integer val = it.next();
				if(count==0){if(another.cycle.containsKey(val)) return false;}
				else if(cycle.containsKey(val)) return false;
			}
			if(count==0) {it = another.iterator();count=1;}
			}
			return true;
		}
		public boolean isIdentity(){return cycle.size()<=1?true:false;}
		public Iterator<Integer> iterator(){return new CycleIterator();}
		public String toString(){
			if(cycle.size()==0) return "()";
			StringBuilder sb = new StringBuilder ("(");
			String com = ",";
			Iterator<Integer> it = iterator();
			while(it.hasNext()) {
				Integer val = it.next();
				sb.append(val);
				if(it.hasNext()) sb.append(com);
			}
			sb.append(")");
			return sb.toString();
		}
		public static Cycle generateCycle (int start, int length) throws IllegalArgumentException {
			if(start<0) throw new IllegalArgumentException ("\nOnly non-negative start argument permitted!");
			if(length<=1) return new Cycle();
			Cycle cycle = new Cycle ();
			int length1 = length+start;
			for (int i = start; i < length1-1; i++) cycle.add(i, i+1);
			cycle.add(length1-1, start);
			return cycle;
		}
		private class CycleIterator implements Iterator<Integer> {
			boolean firstEn = true;
			Integer current;
			CycleIterator(){
				current = first;
			}
			
			public boolean hasNext() {return firstEn?true:current.equals(first)?false:true;}

			
			public Integer next() {
				if(firstEn) firstEn = false;
				Integer cp = current;
				current = getValue(current);
				return cp;
			}

			
			public void remove() {}
			
		}
	}
	public static void main(String[] args){
		
		SymmetricGroup2<Object> cycle = new SymmetricGroup2<Object> (new int[]{0,0,1,0,2});
		System.out.println(cycle);
		//AbstractMatrix<Rational> mat = cycle.constructPermutatMat(Rational.ONE), mat2 = new AbstractMatrix<Rational> (mat);
		//System.out.println(mat);
		SymmetricGroup2<Object> cyc = new SymmetricGroup2<Object> (cycle),id = new SymmetricGroup2<Object> ();
		//SymmetricGroup2<Object> trp = new SymmetricGroup2<Object> (new int[]{2,5});
		int i = 1;
		long start1 = 0, start2 = 0, end1 = 0, end2 = 0;
		double meanCompTimeCycle = 0, meanCompTimeMatrx = 0;
		while (!cyc.equals(id)) {
			StringBuilder sb = new StringBuilder(String.format("pi^%2$d =\t\t\t%1$s",cyc,i));
			sb.append("\n");
			if(i!=1){
				double compCycle = ((double) end1-start1)*1e-9;
				//double compMatrx = ((double) end2-start2)*1e-9;
				sb.append(String.format("exe time (cycle operation):\t%1$g sec",compCycle));
				//sb.append("\n");
				//sb.append(String.format("exe time (matrix operation):\t%1$g sec",compMatrx));
				sb.append("\n");
				meanCompTimeCycle += compCycle;
				//meanCompTimeMatrx += compMatrx;
			}
			//long start1 = System.nanoTime();
			//SymmetricGroup2<Object> conj = trp.multiply(cyc.multiply(trp));
			//long end1   = System.nanoTime();
			//System.out.println(String.format("%1$s pi %1$s =\t%2$s",trp.toString(),conj.toString()));
			
			//sb.append(String.format("exe time: %1$g",((double) end1-start1)*1e-9));
			//sb.append("\n");
			//System.out.println();
			//System.out.println(conj.multiply(cyc).inverse().multiply(conj.inverse()));
			//AbstractMatrix<Rational> co   = cyc.constructPermutatMat(Rational.ONE,cycle.maxArg);
			//long start2 = System.nanoTime();
			//AbstractMatrix<Rational> testMat = cyc.constructPermutatMat(Rational.ONE, cycle.maxArg);
			//if(!mat.equals(testMat))
			//	System.err.println(String.format("Matrix mismatch - wrong matrix\n%1$s",mat.toString()));
			//sb.append(String.format("permutation matrix:\n%1$s",testMat));
			//System.out.println();
			//if(cyc.isKernel()) {System.out.println(sb.toString());System.out.flush();}
			//else {System.err.println(sb.toString());System.err.flush();}
			
			//System.out.println(String.format("mat(pi^%3$d) = \n%1$s\n%2$g",prod.toString(),((double) end2 - start2)*1e-9,i));
			if(i==8)
				System.gc();
			start1 = System.nanoTime();
			cyc = cyc.multiply(cycle);
			end1 = System.nanoTime();
			//start2 = System.nanoTime();
			//mat = mat.multiply(mat2);
			//end2 = System.nanoTime();
			i++;
			System.gc();
		}
		System.out.println(String.format("order computed1: %1$d \t\nmean exe time (cycle):\t%2$g sec\nmean exe time (matrx):\t%3$g sec",i,meanCompTimeCycle/i,meanCompTimeMatrx/i));
	}
}
