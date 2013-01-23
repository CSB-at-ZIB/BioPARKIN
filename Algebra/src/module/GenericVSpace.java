package module;

import java.util.Iterator;
import java.util.Map.Entry;
import java.util.TreeMap;

import field.AbstractField;
import group.AbstractAbel;

public class GenericVSpace<F extends AbstractField<F>> extends AbstractAbel<GenericVSpace<F>>implements VectorSpace<GenericVSpace<F>,F>{
	private TreeMap<Integer,F> coeffMap;
	public GenericVSpace (){super();coeffMap = new TreeMap<Integer,F>();}
	public GenericVSpace (F[] array){this(); for (int i = 0; i < array.length; i++) {if(array[i]!=null) this.setEntry(i, array[i]);}}
	public GenericVSpace(GenericVSpace<F> vector){
		this();
		for (Entry<Integer,F> entry:vector){
			F coeff;
			if(!(coeff = entry.getValue()).isZero()) coeffMap.put(entry.getKey(), coeff); 
		}
	}
	public GenericVSpace<F> multiply(F scalar) {
		GenericVSpace<F> slrProd = new GenericVSpace <F> ();
		for (Entry<Integer,F> entry:coeffMap.entrySet()) slrProd.coeffMap.put(entry.getKey(), entry.getValue().multiply(scalar));
		return slrProd;
	}

		
	public GenericVSpace<F>ringAct(F scalar) {return multiply(scalar);}

	
	public GenericVSpace<F> add(GenericVSpace<F> another) {
		GenericVSpace<F> sum = new GenericVSpace <F> ();
		for (Entry<Integer,F> entry:coeffMap.entrySet()) sum.coeffMap.put(entry.getKey(), entry.getValue());
		for (Entry<Integer,F> entry:another.coeffMap.entrySet()) {
			Integer key = entry.getKey();
			F sumEntry;
			if((sumEntry = sum.coeffMap.get(key))!=null) {
				sumEntry = sumEntry.add(entry.getValue());
				if(!sumEntry.isZero()) sum.coeffMap.put(key, sumEntry);
				else sum.coeffMap.remove(key);
			} else sum.coeffMap.put(key, entry.getValue()); 
		}
		return sum;
	}

	
	public boolean equals(GenericVSpace<F> another) {if(this==another) return true; return coeffMap.equals(another.coeffMap)?true:false;}

	
	public void clear() {coeffMap.clear();}

	
	public F getValue(int index) {
		F coeff;
		return (coeff = coeffMap.get(index))==null?null:coeff;
	}

	
	public Integer getIndex(F val) {
		for (Entry<Integer,F> entry:this) {if(entry.getValue().equals(val)) return entry.getKey();}
		return null;
	}

	
	public void setEntry(int index, F value) {
		if(index>=0&&value!=null){
			if(!value.isZero()) coeffMap.put(index, value);
		}
	}

	public boolean isZero (){
		for (Entry<Integer,F> entry:this) {if(!entry.getValue().isZero()) return false;}
		return true;
	}
	
	public Iterator<Entry<Integer, F>> iterator() {return coeffMap.entrySet().iterator();}
	
	public F remove(int index) {return coeffMap.get(index);}
	
	public String toString(){
		if(coeffMap.size()==0) return "0";
		StringBuilder sb = new StringBuilder ("(");
		String comma = ",", zero = "0";
		int lastKey = coeffMap.lastKey();
		for (int i = 0; i <= lastKey;i++){
			F coeff;
			if((coeff = getValue(i))!=null) sb.append(coeff.toString());
			else sb.append(zero);
			if(i!=lastKey) sb.append(comma);
		}
		sb.append(")");
		return sb.toString();
	}
	
}