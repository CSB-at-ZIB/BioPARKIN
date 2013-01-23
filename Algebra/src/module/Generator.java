package module;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.Set;

import ring.Ring;
/**
 * The module generator class - contains a set of generators,
 * such that the underlying module of type <code>R</code> is spanned
 * @author bzfmuell
 *
 * @param <M> the <code>R</code> module type to span
 * @param <R> the ring type
 */
public class Generator<M extends Module<M,R>, R extends Ring<R>> implements Iterable<Entry<Integer,M>>{
	/**the generator set*/
	private HashMap<Integer,M> generatorSet;
	/**
	 * Constructs the generator set. <b>Note</b>, if <tt>moduleElement[i].equals(moduleElement[j])</tt>
	 * returns true for some indices <tt>0 &#8804 i &lt j &#8804 modulelement.length-1</tt> then the
	 * <tt>j</tt>-th component will not be added
	 * @param moduleElements an array of generators
	 */
	public Generator (M[] moduleElements){
		generatorSet = new HashMap<Integer,M> ();
		int count = 0;
		for (M element:moduleElements){
			if(!generatorSet.containsValue(element)) {if(!element.isZero()){generatorSet.put(count, element);count++;}}
		}
	}
	/**
	 * Constructs a generator set 
	 * @param generatorSet
	 */
	public Generator (Set<M> generatorSet){
		this.generatorSet = new HashMap<Integer,M> (generatorSet.size());
		int count = 0; 
		for (M element:generatorSet) if(!element.isZero()){this.generatorSet.put(count,element);count++;}
	}
	/**
	 * Returns the generator set as a {@link HashSet}
	 * @return
	 */
	public HashSet<M> getGeneratorSet (){return new HashSet<M>(generatorSet.values());}
	public Iterator<Entry<Integer,M>> iterator (){return generatorSet.entrySet().iterator();}
	
	/**
	 * Returns the rank of this generator set, to specify its
	 * cardinality
	 * @return the rank
	 */
	public int rank (){return generatorSet.size();}
}
