/*
 * Created on 20-lug-2005
 *
 * To change the template for this generated file go to
 * Window&gt;Preferences&gt;Java&gt;Code Generation&gt;Code and Comments
 */
package py4j;

import java.util.ArrayList;
import Jama.Matrix;
import py4j.GatewayServer;

public class Grey implements IFilter{
	
	public IFilter genFilter(){
		return new Grey();
	}
	public Double nextValue(ArrayList<Double> valueSet){//, double costante){
		int costante=0;
		if (valueSet.size()<4){
			if(valueSet.size()==0){
				return null;
			}
			return valueSet.get(valueSet.size() - 1);
		}
		double[][] valX1=new double[1][valueSet.size()]; // 1 riga, n colonne
		for(int i=0;i<valueSet.size();i++){
			double xi=0;
			for(int a=0;a<=i;a++){
				if(valueSet.get(a)==null)return null;
				xi=xi+(((Double)valueSet.get(a)).doubleValue()+costante);
			}
			valX1[0][i]=xi; // riga 1, colonna i
		}
		Matrix X1=new Matrix(valX1);
		double[][] valB=new double[valueSet.size()-1][2];
		for(int x=0;x<valueSet.size()-1;x++){
			valB[x][0]=-0.5*(X1.get(0,x)+X1.get(0,x+1));
			valB[x][1]=1;
		}
		Matrix B=new Matrix(valB);
		Matrix Bt=B.transpose();
		Matrix BtB=Bt.times(B);
		Matrix BtB_1=BtB.inverse();
		Matrix C=BtB_1.times(Bt);
		double[][] valYn=new double[valueSet.size()-1][1];
		for(int i=1;i<valueSet.size();i++){
			valYn[i-1][0]=valueSet.get(i); // riga 1, colonna i
		}
		Matrix Yn=new Matrix(valYn);
		Matrix au=C.times(Yn);
		double ris1=x1_(valueSet.size()+1,au.get(0,0),au.get(1,0),X1.get(0,0));
		double ris2=x1_(valueSet.size(),au.get(0,0),au.get(1,0),X1.get(0,0));
		return new Double(ris1-ris2-costante);
	}
	
	private double x1_(int k,double a,double u,double x1){
		if(a<0&&a>-0.000000000001)a=-0.000000000001;
		if(a>=0&&a<0.000000000001)a=0.000000000001;
	        double x1_=(x1-u/a)*Math.exp((-a)*(double)k);
		return x1_;
	}
	
	 public static void main(String[] args) {
        GatewayServer gatewayServer = new GatewayServer(new Grey());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }
}
