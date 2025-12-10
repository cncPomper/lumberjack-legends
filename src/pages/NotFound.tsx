import { useLocation } from "react-router-dom";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { Home, Axe } from "lucide-react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      {/* Background */}
      <div 
        className="fixed inset-0 -z-10"
        style={{
          background: 'linear-gradient(180deg, hsl(200 30% 15%) 0%, hsl(140 30% 12%) 40%, hsl(25 30% 10%) 100%)',
        }}
      />
      
      <div className="text-center animate-slide-up">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-muted mb-6">
          <Axe className="w-10 h-10 text-muted-foreground" />
        </div>
        
        <h1 className="text-6xl font-heading font-bold text-gradient-gold mb-4">404</h1>
        <p className="text-xl text-muted-foreground mb-8">
          Oops! This tree doesn't exist in our forest.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link to="/">
            <Button variant="gold" size="lg">
              <Home className="w-5 h-5 mr-2" />
              Back to Home
            </Button>
          </Link>
          <Link to="/play">
            <Button variant="outline" size="lg">
              <Axe className="w-5 h-5 mr-2" />
              Play Game
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
