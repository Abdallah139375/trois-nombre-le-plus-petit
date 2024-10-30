using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace trois_nombre_le_plus_petit
{
    class Program
    {
        static void Main(string[] args)
        {
            // declarations 
            double nb1,nb2 ,nb3;

            //saisie de trois nombre 

            Console.WriteLine("entrez un premier nombre = ");
            nb1 = double.Parse(Console.ReadLine());
            Console.WriteLine("entrez un deuxieme nombre = ");
            nb2 = double.Parse(Console.ReadLine());
            Console.WriteLine("entrez un troisiéme nombre = ");
            nb3 = double.Parse(Console.ReadLine());

            //afficher le plus petit des trois nombres 
            Console.WriteLine("le plus petit des trois est " + Math.Min(nb1, Math.Min(nb2, nb3)));
            Console.ReadLine();

        }
        

    }
}
