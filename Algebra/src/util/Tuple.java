package util;

import java.util.Iterator;
import java.util.Map.Entry;
import java.util.TreeMap;
/**
 * The tuple class: note any instance of this class is a mutable object.
 * To use objects of this class as keys in {@link java.util.Map}s implement
 * a final subclass overriding the {@link Tuple#clear()} and {@link Tuple#setEntry(int, Object)}
 * as follows:<br />
 * <tt>public void setEntry (int index, X value){}</tt><br />
 * <tt>public void clear (){}</tt>
 * <br />Although, upcasting renders the object mutable
 * @author gmueller
 *
 * @param <X>
 */
public class Tuple<X> implements Tupleable<X>{
	/**a sorted map of all tuple entries*/
	private TreeMap<Integer,X> tuple;
	/**
	 * Constructs the default (empty) tuple object
	 */
	public Tuple (){tuple = new TreeMap<Integer,X> ();}
	/**
	 * Constructs the tuple <tt>(tuple[0],...,tuple[tuple.length-1])</tt>,
	 * where <tt>tuple</tt> is the argument array. <b>Note</b>, that null
	 * entries are ignored.
	 * @param tuple the argument array
	 */
	public Tuple (X[] tuple){
		this();
		for (int i = 0; i < tuple.length;i++) if(tuple[i]!=null) this.tuple.put(i, tuple[i]);
	}
	/**
	 * Removes all entries from this tuple
	 */
	public void clear (){tuple.clear();}
	/**
	 * Returns true if and only if <tt>o</tt> is of same
	 * type and all its entries (with exactly the same index)
	 * are present in both instances
	 */
	@Override
	public boolean equals (Object o){
		if(o == this) return true;
		if(!(o instanceof Tuple)) return false;
		@SuppressWarnings("unchecked")
		Tuple<X> cp = (Tuple<X>) o;
		return tuple.equals(cp.tuple)?true:false;
	}
	public Integer getIndex (X val){
		for (Entry<Integer,X> entry:this) if(entry.getValue().equals(val)) return entry.getKey();
		return null;
	}
	/**
	 * Returns the value associated with the <tt>index</tt>
	 * or null if no such entry exists
	 * @param index the index
	 * @return the value
	 */
	public X getValue (int index){X value; return (value = tuple.get(index))==null?null:value;}
	@Override
	public int hashCode (){
		int hash = 0;
		for (Entry<Integer, X> entries:this) hash += (2*entries.getKey()+1)*entries.getValue().hashCode();
		return hash;
	}
	public Iterator<Entry<Integer, X>> iterator() {return tuple.entrySet().iterator();}
	public X remove (int index){
		X entry = tuple.get(index);
		return entry==null?null:entry;
	}
	/**
	 * Sets the entry at position <tt>index</tt> to <tt>value</tt> only
	 * if <code>(value!=null)</code> returns true
	 * @param index the index
	 * @param value the value (non null!)
	 * @throws IndexOutOfBoundsException negative index
	 */
	public void setEntry (int index, X value) throws IndexOutOfBoundsException {
		if(index<0) throw new IndexOutOfBoundsException ("\nNegative index: "+index);
		if(value!=null) tuple.put(index, value);
	}
	
	/**
	 * Returns a string representation of this tuple object
	 */
	@Override
	public String toString (){
		StringBuilder sb    = new StringBuilder ("(");
		String        comma = ","; 
		Iterator<Entry<Integer,X>> it = iterator();
		while (it.hasNext()) {
			Entry<Integer,X> entry = it.next();
			sb.append(entry.getValue().toString());
			if(it.hasNext()) sb.append(comma);
		}
		sb.append(")");
		return sb.toString();
	}
}
